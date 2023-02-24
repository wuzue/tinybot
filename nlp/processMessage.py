from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy

app = Flask(__name__)
CORS(app)
nlp = spacy.load("en_core_web_sm")

@app.route("/process_message", methods=["POST"])
def process_message():
  try:
    message = request.json["message"]
  except KeyError:
    return jsonify({"error": "Missing 'message' key in request payload"}), 400
  #process msg using spacy
  doc = nlp(message)
  #convert set to list
  # entities = list(doc.ents)
  entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
  #return result in json
  return jsonify({"entities": entities})

if __name__ == '__main__':
  app.run(debug=True, use_reloader=False)
