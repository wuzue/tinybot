from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

#english language model
modelEN = spacy.load("en_core_web_sm")
#portuguese language model
modelPT = spacy.load("pt_core_news_sm")

@app.route('/', methods=['GET', 'POST'])
def home():
    msg = request.json.get('message')
    response = 'processed msg: ' + msg
    print(response)
    text = msg
    # change here depending on the language you want to process
    doc = modelEN(text)
    # tokens = []
    output_str = ""
    for token in doc:
      # tokens.append({"text": token.text, 'pos': token.pos_})
      output_str += f"{token.text} {token.pos_}"
    # print(output_str)
      # print(token.text, token.pos_)
    # return jsonify(tokens)
    return output_str

if __name__ == '__main__':
    print('starting flask')
    app.run(port=5000)
