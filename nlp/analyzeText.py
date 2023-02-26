# What does this code do?
# It simply receives a message from user (via chat, i.e front-end), and then analyze every word
# in that sentence, and then answer back the classification of that word.
# We send: "a green apple"
# We get back: "a DET, green ADJ, apple NOUN"

from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# load language models
modelEN = spacy.load("en_core_web_sm") #english model
modelPT = spacy.load("pt_core_news_sm") #portuguese model

@app.route('/', methods=['GET', 'POST'])
def home():
    msg = request.json.get('message')
    response = 'processed msg: ' + msg
    print(response)
    text = msg
    # change here depending on the language you want to process
    doc = modelEN(text)
    output_str = ""
    for token in doc:
      output_str += f"{token.text} {token.pos_}" + " "
    return output_str

if __name__ == '__main__':
    print('starting flask')
    app.run(port=5000)
