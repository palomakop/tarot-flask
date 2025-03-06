# flask --app app_psycop2_db run

from flask import Flask, jsonify, request
import os, psycopg2, json, requests

app = Flask(__name__)

with open('decks.json') as f:
    decks = json.load(f)

databaseUrl = os.environ['DATABASE_URL']
conn = psycopg2.connect(databaseUrl)

# class Pull(db.Model):
#     id = db.Column(db.String(20), primary_key=True)
#     spread_type = db.Column(db.String(20), unique=False, nullable=False)
#     number_of_cards = db.Column(db.Integer, nullable=False)
#     intention = db.Column(db.String(100), unique=False, nullable=False)
#     created_time = db.Column(db.DateTime, unique=False, nullable=False)



def pullRandomCards():
    return "cards"

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message':'Hello, world','success':'true'})

@app.route('/create-pull', methods=['POST'])
def createPull():
    pullDetails = request.json
    spreadType = pullDetails['spreadType']
    numberOfCards = pullDetails['numberOfCards']
    deck = pullDetails['deck']
    intention = pullDetails['intention']
    pull = {
        'pullDetails': pullDetails
    }
    # for i in range(numberOfCards):
    #     pull['cards'][i] = 
    return jsonify({'message':pull,'success':'true'})