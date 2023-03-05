from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import spacy
from duckduckgo_search import ddg, ddg_videos, ddg_answers, ddg_news
import requests
# from transformers import AutoModel, AutoTokenizer

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

"""     refer to tinygrad, and move this part to a separate file later
model_name = 'bert-base-uncased'
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

demo_text = 'this is a sample data'
demo_input = tokenizer(demo_text, return_tensors='pt')
"""

greetings = ['hi', 'hello', 'hey', 'yo', 'greetings', 'heya', "what's up", 'what up', 'wassup'] # greeting words, add more if necessary
how_are_you = ['how are you?', 'how are you', 'how are you doing?', 'how are you doing', 'how are you today?', 'how are you today', 'what is up with you?', 'what is up with you', 'whats up with you?', 'whats up with you', "what's up with you?", "what's is up with you"]
what_can_you_do = ["what can you do?", "what can you do", "what can u do", "what can u do?", "tell me what can you do"]
request_verbs = ['search', 'i need', 'tell me', 'tell', 'what is', 'what', 'how to'] # verbs that indicate a request for information, add more if necessary
request_verbs_videos = ['a video of', 'youtube video', 'video about', 'youtube video about', 'video']
small_talk = {
  "greetings": ["Hello!", "Hi there!", "Hey! How can I assist you today?", "Howdy!", "Hey!"], # response for greetings, add more if necessary
  "bot_info": [""],
  "thanks": ["You're welcome!", "No problem!", "Glad to assist you!"],
  "bot_is_doing": ["I'm doing great, thanks for asking!", "I'm feeling a bit tired today, but still ready to chat!", "I'm doing well, how about you?",    "I'm doing just fine, thanks!",    "I'm having a great day, thanks for asking!",    "I'm feeling a little under the weather, but I'm here to help!",    "I'm doing awesome today, thanks for asking!",    "I'm feeling a little overwhelmed, but I'm always here to chat with you!",    "I'm doing pretty well, thanks for asking!",    "I'm feeling fantastic today, thanks for asking!",    "I'm doing okay, how about you?",    "I'm feeling a little stressed, but I'm happy to chat with you!",    "I'm doing wonderfully today, thanks for asking!",    "I'm feeling a bit anxious today, but I'm here to help you!",    "I'm doing great, thanks for checking in!"],
  "who_is_bot": ["I'm a chatbot designed to assist you with information. What can I help you with?", "I'm your friendly chatbot!",    "I'm an AI language model here to chat with you.",    "I'm your virtual assistant, at your service!",    "I'm a machine learning model designed to converse with humans.",    "I'm a language AI created by OpenAI.",    "I'm an intelligent chatbot designed to help you.",    "I'm a digital assistant programmed to answer your questions.",    "I'm an artificial intelligence programmed to have conversations with people.",    "I'm a computer program designed to interact with you.",    "I'm an AI language model, how can I assist you?",    "I'm a chatbot designed to help you with your inquiries.",    "I'm an automated assistant programmed to respond to your queries.",    "I'm a virtual companion, ready to chat with you!",    "I'm an intelligent assistant designed to assist you with your needs.",    "I'm a digital agent here to help with any questions or concerns you may have."],
  "bot_can_do": ["I can help you with information and answer your questions. Just ask me anything!", "I can do many things! For example, I can search the web for you, give you the latest news, or even tell you a joke. What would you like me to do?", "I'm designed to assist you with information. You can ask me anything from general knowledge to specific topics like sports, entertainment, or technology.", "I can do a lot! I can answer questions, give recommendations, help you find information, and more. Just let me know what you need.", "I'm a chatbot, so I'm here to chat with you and help you with your needs. Whether it's finding information or just having a conversation, I'm here for you."]
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
  
  # ask bot how its doing
  for token in doc:
    if text in how_are_you:
      intent = 'how_are_you_doing'
      break
  
  # ask what can the bot do
  for token in doc:
    if text in what_can_you_do:
      intent = "can_you_do"
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
  
  #check for news request
  for i, token in enumerate(doc):
    if token.text.startswith('news'):
      keywords = ' '.join([t.text for t in doc[i+1:]])
      intent = 'news_request'
    elif token.text.startswith('news about'):
      keywords = ' '.join([t.text for t in doc[i+2:]])
      intent = 'news_request'
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
      elif token.text == 'who' and token.nbor().text == 'are' and token.nbor(2).text == 'you' or text == 'who are you?' or text == 'who are you' or text == 'who r u' or text == 'who r u?' or text == 'who is you' or text == 'who is you?' or text == 'whos you' or text == 'whos you?':
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

  # response for how are you?
  elif intent == 'how_are_you_doing':
    response = random.choice(small_talk['bot_is_doing'])

  elif intent == "can_you_do":
    response = random.choice(small_talk['bot_can_do'])

  # response for news request
  elif intent == 'news_request':
    result = ddg_news(keywords, region='wt-wt', safesearch='Off', time='d', max_results=100)
    response = f"{result[0]['title']}\n\n {result[0]['body']}\n\n Link: {result[0]['url']}\n\n Source: {result[0]['source']}\n\n{result[1]['title']}\n\n {result[1]['body']}\n\n Link: {result[1]['url']}\n\nSource: {result[1]['source']}"

  # response for searching | `search machine learning`
  elif intent == 'request_information':
    #default ddg answers
    # result = ddg(keywords, region='wt-wt', safesearch='Off', max_results=2, time='y')
    # ddg instant answers
    result = ddg_answers(keywords, related=True)
    # response = f"I found this about {keywords}:\n\n {result[0]['title']}\n\n {result[0]['body']}\n\nHere you can read more about it:\n{result[0]['href']}"
    response = f"{result[0]['text']}"
  
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
    response = random.choice(small_talk['who_is_bot'])
  
  # response when asking for coin price | bitcoin price
  elif intent == 'crypto':
    response = f"The current price for {text.split()[0]} is: ${coin_price:.2f}."

  # response when asking for crypto price wrongly
  elif intent == 'help_crypto':
    response = "Correct syntax is: coin + price. For example: bitcoin price"

  # response when none of the conditions above are met
  else:
    response = "I am sorry, as a new bot, I don't understand this yet."

  # return jsonify({'response': response}) # this returns json
  return response

if __name__ == '__main__':
  app.run(debug=True)