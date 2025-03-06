# tarot-flask

A Flask API to support a tarot web app.

## Setup

Install Flask and create a Python virtual enviromnent according to the requirements in `requirements.txt`. If running on Heroku, this is done automatically.

This project uses supabase as the database and the Random.org API for generating true random numbers based on atmospheric EMF. API keys for both, and the URL for a supabase instance, must be set as enviroment variables.

To run the project in a development environment, use `flask run` from the project folder after activating the virtual environment.

## Routes

### `GET` /

Just returns a hello world json message to show the API is running.

### `POST` /pull/new

Request body example:

```json
{
    "spreadType": "Single", // a string to describe the card layout for front end
    "numberOfCards": 1, // how many cards should be randomly pulled
    "deck": "Rider-Waite-Smith", // must be present in decks.json - currently only this one
    "allowReversed": true, // if false, cards will never be pulled as reversed
    "intention": "What will the weather be tomorrow?" // optional
}
```

Example response:

```json
{
    "message": {
        "cards": [
            {
                "description": "Wands flying through the air, symbolizing speed and progress",
                "element": "Fire",
                "filename": "wands8",
                "reversed": false,
                "reversedMeaning": "Delays, slowed progress",
                "suit": "Wands",
                "suitIndex": "8",
                "title": "Eight of Wands",
                "uprightMeaning": "Speed, progress"
            }
        ],
        "id": "ajutsm3wrn",
        "pullDetails": { // contains the data from the initial request
            "allowReversed": true,
            "deck": "Rider-Waite-Smith",
            "intention": "What will the weather be tomorrow?",
            "numberOfCards": 1,
            "spreadType": "Single"
        },
        "timestamp": "2025-03-05 21:18:38.883712+00:00"
    },
    "success": "true"
}
```

### `GET` /pull/`{id}`

Use a GET request to this endpoint to get a pull that was created previously, using the `id` value returned by `/create-pull`. The response structure is identical to the one returned by `/create-pull`.

## Future ideas

- Integrate authentication so that pulls from a logged-in user will be associated with their account. (Supabase has built-in auth)
- Add methods to delete a pull or edit the intention (requires auth).
