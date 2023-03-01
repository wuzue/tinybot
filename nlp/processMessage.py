from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import spacy
from duckduckgo_search import ddg
from duckduckgo_search import ddg_videos
import requests

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

greetings = ['hi', 'hello', 'hey', 'yo', 'greetings', 'heya', "what's up", 'what up', 'wassup'] # greeting words, add more if necessary
request_verbs = ['search', 'i need', 'tell me', 'tell', 'what is', 'what', 'how to'] # verbs that indicate a request for information, add more if necessary
request_verbs_videos = ['a video of', 'youtube video', 'video about', 'youtube video about', 'video']
small_talk = {
  "greetings": ["Hello!", "Hi there!", "Hey! How can I assist you today?", "Howdy!", "Hey!"], # response for greetings, add more if necessary
  "bot_info": ["I'm a chatbot designed to assist you with information. What can I help you with?"],
  "thanks": ["You're welcome!", "No problem!", "Glad to assist you!"],
  # Add more small talk phrases and responses as needed
}

modelEN = spacy.load("en_core_web_sm") #english model

@app.route('/process-message', methods=['GET','POST'])
def process_message():
  message = request.json.get('message')
  text = message.lower()
  doc = modelEN(text) 
  intent = None
  entity_type = None
  entity_value = None

  #coingecko api
  crypto_url = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=90&page=1&sparkline=false")
  crypto_list = crypto_url.json()
  # extract name of coins
  crypto_names = [crypto['name'].lower() for crypto in crypto_list]

  # check for greetings 
  for token in doc:
    if token.pos_ == 'INTJ' and token.dep_ == 'intj' or token.pos_ == 'INTJ' and token.dep_ == 'ROOT' or token.text in greetings: 
      intent = 'greetings'
      break
  
  #ask for crypto price
  for token in doc:
    if text.split()[0] in crypto_names and text.split()[1] == 'price':
      coin_data = next((coin for coin in crypto_list if coin['name'].lower() == text.split()[0].lower()), None)
      if coin_data:
        coin_price = coin_data['current_price']
        # response = f"The current price of {text.split()[0]} is {coin_price:.2f} USD"
        intent = 'crypto'
      else:
        response = f"I am sorry, I couldn't find the price for {text.split()[0]}. Please, try another coin."
      break
    elif token.text in crypto_names and text.split()[0]:
      intent = 'help_crypto'
    
  # check for request information
  for i, token in enumerate(doc):
    if token.text in request_verbs:
      if token.text.startswith('what'):
        keywords = ' '.join([t.text for t in doc[i+2:]])
      elif token.text == 'tell me what is':
        keywords = ' '.join([t.text for t in doc[i+4:]])
      elif token.text.startswith('tell'):
        keywords = ' '.join([t.text for t in doc[i+2:]])
      else:
        keywords = ' '.join([t.text for t in doc[i+1:]])
      intent = 'request_information'
      break
  
  # this one is to search for pdf files
  for i, token in enumerate(doc):
    if token.text == 'pdf':
      keywords = ' '.join([t.text for t in doc[i+1:]]) + ':pdf'
      intent = 'pdf_files'
      break

  # this one is to search for youtube video | this is kinda inaccurate lol]
  # request_verbs_videos = ['a video of', 'youtube video', 'video about', 'youtube video about']
  for i, token in enumerate(doc):
    if token.text in request_verbs_videos:
      if token.text.startswith('video'):
        keywords = ' '.join([t.text for t in doc[i+1:]])
      else:
        keywords = ' '.join([t.text for t in doc[i+1:]])
      intent = 'video_search'

  # check for customer support inquiries
  for token in doc:
    if token.text == 'help' or token.text == 'support' or token.text == 'problem' or token.text == 'issue':
      intent = 'customer_support'
      break

  # check for small talk
  if intent is None:
    for token in doc:
      if token.text == 'thanks' or token.text == 'thank' or token.text == 'thank you':
        intent = 'thanks'
        break
      elif token.text == 'who' and token.nbor().text == 'are' and token.nbor(2).text == 'you':
        intent = 'bot_info'
        break
  
  # extract named entities, but this extracts all the word e.g. deep learning = 2
  entities = []
  for ent in doc.ents:
    entity_type = ent.label_
    entity_value = ent.text
    entities.append((entity_type, entity_value))
  # use the first named entity for now (can be modified)
  if entities:
    entity_type, entity_value = entities[0]
  else:
    entity_type, entity_value = None, None

  # GENERATE RESPONSES
  # response for greetings
  if intent == 'greetings':
    response = random.choice(small_talk['greetings'])

  # response for searching | `search machine learning`
  elif intent == 'request_information':
    # print(keywords)
    result = ddg(keywords, region='wt-wt', safesearch='Off', max_results=2, time='y')
    response = f"I found this about {keywords}:\n\n {result[0]['title']}\n\n {result[0]['body']}\n\nHere you can read more about it:\n{result[0]['href']}"
  
  # response for searching for pdf files | `pdf machine learning`
  elif intent == 'pdf_files':
    result = ddg(keywords, safesearch='Off', max_results=100)
    extracted_keyword = keywords.split(":")[0]
    response = f"I found this pdf for {extracted_keyword}: \n\n {result[0]['title']}\n\n {result[0]['body']}\n\nHere is the link for it:\n{result[0]['href']}"

  # response for searching for video
  elif intent == 'video_search':
    result = ddg_videos(keywords, region='wt-wt', safesearch='Off',max_results=50)
    response = f"Here's a video about: {keywords}\n\n {result[0]['title']}\n\n {result[0]['description']}\n\nHere is the link for the video:\n{result[0]['content']}"

  # response for help
  elif intent == 'customer_support':
    response = "I'm sorry to hear that. Please provide more details about your problem or issue."

  # response for thanking the bot
  elif intent == 'thanks':
    response = random.choice(small_talk['thanks'])

  # response when asking the bot about itself
  elif intent == 'bot_info':
    response = random.choice(small_talk['bot_info'])
  
  elif intent == 'crypto':
    response = f"The current price for {text.split()[0]} is: ${coin_price:.2f}."

  elif intent == 'help_crypto':
    response = "Correct syntax is: coin + price. For example: bitcoin price"

  # response when none of the conditions above are met
  else:
    response = "I am sorry, I did not understand your request."

  # return jsonify({'response': response}) # this returns json
  return response

if __name__ == '__main__':
  app.run(debug=True)