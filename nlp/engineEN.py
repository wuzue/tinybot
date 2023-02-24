import spacy

#loading ENG language model
nlp = spacy.load("en_core_web_sm")

#loading PT language model
# nlp = spacy.load("pt_core_web_sm")

#defining input text
text = "Hello, how are you today?"

#process text with NLP pipeline
doc = nlp(text)

#print tokens and their part-of-speech tags
for token in doc:
  print(token.text, token.pos_)