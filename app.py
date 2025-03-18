from flask import Flask, jsonify, request
from supabase import create_client, Client
from datetime import datetime, timezone
import os, psycopg2, json, requests, random, string
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",
            "https://subtle.cards",
            r"https://.*\.netlify\.app"
        ]
    }
})

with open('decks.json') as f:
    decks = json.load(f)

RANDOMORG_KEY = os.environ.get("RANDOMORG_KEY")
RANDOMORG_HOST = 'https://api.random.org/json-rpc/4/invoke'

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def generateRandomString(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generateIntegerSequences(length, totalCards):
    body = {
        'jsonrpc': '2.0',
        'method': 'generateIntegerSequences',
        'params': {
            'apiKey': RANDOMORG_KEY,
            'n': 2,
            'length': length,
            "min": [1, 0],
            "max": [totalCards, 1],
            "replacement": [False, True]
        },
        "id": random.randint(10000, 99999)
    }
    message = requests.post(RANDOMORG_HOST, json=body).json()
    return message

def pullCards(arrays, deck, allowReversed):
    cards = []
    for n in range(0,len(arrays[0])):
        card = decks[deck]['cards'][arrays[0][n]-1]
        if arrays[1][n] == 1 and allowReversed:
            card['reversed'] = True
        else:
            card['reversed'] = False
        cards.append(card)
    return cards

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message':'Hello, world','success':'true'})

# example json body for create-pull
# {
#     "spreadType":"Single", # "Triple" or "Celtic Cross" - anything as long as it's implemented in front end
#     "numberOfCards":1, # or 3 or 6 or whatever
#     "deck":"Rider-Waite-Smith", # currently the only deck
#     "allowReversed":true,
#     "intention":"What will the weather be tomorrow?", # a user defined string, optional
# }

@app.route('/pull/new', methods=['POST'])
def createPull():
    pullId = generateRandomString(10)
    pullDetails = request.json
    pull = {
        'pullDetails': pullDetails,
        'id': pullId,
        'timestamp': str(datetime.now(timezone.utc))
    }

    # call to random.org api
    randomOrgResponse = generateIntegerSequences(pullDetails['numberOfCards'], decks[pullDetails['deck']]['totalCards'])
    randomInts = []
    # check random.org api response for errors - perhaps should add a fallback using math.random
    if 'result' in randomOrgResponse:
        randomInts = randomOrgResponse['result']['random']['data']
    elif 'error' in randomOrgResponse:
        return jsonify({'message':{'randomOrgResponse': randomOrgResponse},'success':'false'})
    else:
        return jsonify({'message':'unknown error','success':'false'})

    # pull cards according to the numbers from random.org
    pull['cards'] = pullCards(randomInts, pullDetails['deck'], pullDetails['allowReversed'])

    # store pull in the supabase
    supabaseResponse = (
        supabase.table("pulls")
        .insert({"id": pullId, "pull": pull})
        .execute()
    )

    return jsonify({'message':pull,'success':'true'})

@app.route('/pull/<string:id>', methods=['GET'])
def getPull(id):
    response = (
        supabase.table("pulls")
        .select("*")
        .eq("id", id)
        .execute()
    )
    pull = json.loads(response.json())['data'][0]['pull']
    return jsonify({'message':pull,'success':'true'})
