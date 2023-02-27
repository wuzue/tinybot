from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import spacy

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

greetings = ['hi', 'hello', 'hey', 'yo', 'greetings', 'heya', "what's up", 'what up', 'wassup'] # greeting words, add more if necessary
request_verbs = ['find', 'get', 'show', 'tell', 'give'] # verbs that indicate a request for information, add more if necessary
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

  # check for greetings 
  for token in doc:
    if token.pos_ == 'INTJ' and token.dep_ == 'intj' or token.pos_ == 'INTJ' and token.dep_ == 'ROOT' or token.text in greetings: 
      intent = 'greetings'
      break

  # check for request information
  # THIS IS KINDA WEIRD, NOT WORKING PROPERLY, CANT DETECT TWO WORDS OF CONTENT E.G. BURGER KING, ONLY DETECTS KING.
  for token in doc:
    if token.text in request_verbs:
      intent = 'request_information'
      break
    elif token.pos_ == 'VERB' and token.dep_ == 'ROOT' and token.text != 'be':
      intent = 'request_information'
      break


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

  # extract named entities
  for ent in doc.ents:
    entity_type = ent.label_
    entity_value = ent.text
    break

  # generate responses
  if intent == 'greetings':
    response = random.choice(small_talk['greetings'])
  elif intent == 'request_information' and entity_type:
    response = f"Here's the information I found on {entity_type}: {entity_value}"
  elif intent == 'customer_support':
    response = "I'm sorry to hear that. Please provide more details about your problem or issue."
  elif intent == 'thanks':
    response = random.choice(small_talk['thanks'])
  elif intent == 'bot_info':
    response = random.choice(small_talk['bot_info'])
  else:
    response = "I am sorry, I did not understand your request."

  # return jsonify({'response': response}) # this returns json
  return response

if __name__ == '__main__':
  app.run(debug=True)