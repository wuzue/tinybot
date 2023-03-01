from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import random
import os
import sys
import requests

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# load language models
modelEN = spacy.load("en_core_web_sm") #english model
modelPT = spacy.load("pt_core_news_sm") #portuguese model

greetings = ['hi', 'hello', 'hey', 'yo', 'greetings', 'heya', "what's up", 'what up', 'wassup']

responses = ['Hello!', 'Hi there!', 'Hey!', 'Howdy!', 'Greetings!']

@app.route('/weather', methods=['GET'])
def weather():
    cityName = request.args.get('message')
    if not cityName:
        return jsonify({"error": "Please provide a valid message."}), 400

    apiKey = os.getenv('APIKEY')
    url = f"http://api.weatherapi.com/v1/current.json?key={apiKey}&q={cityName}&aqi=no"
    response = requests.get(url)
    weatherData = response.json()
    regionName = weatherData['location']['region']
    getCountry = weatherData['location']['country']
    temperature = weatherData['current']['temp_c']

    responseMessage = f"The temperature in {cityName} - {regionName}, {getCountry} is {temperature}°C."
    return jsonify({"message": responseMessage}), 200

@app.route('/', methods=['GET', 'POST'])
def home():
    while True:
      msg = request.json.get('message')
      response = 'processed msg: ' + msg
      print(response)
      text = msg
      # change here depending on the language you want to process
      doc = modelEN(text.lower())
      for token in doc:
        if token.text in greetings:
          if len(doc) > 1 and doc[1].text == 'bot' or len(doc) == 1:
            return random.choice(responses)
          else:
            person = doc[1].text
            return "Uhhh, Hello... But I don't know who " + person.capitalize() + ' is.'
      return "I don't know what " + token.text + ' means.'

if __name__ == '__main__':
    print('starting flask')
    app.run(port=5000)
