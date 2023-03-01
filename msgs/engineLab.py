import spacy

#loading ENG language model
# nlp = spacy.load("en_core_web_sm")

#loading PT language model
nlp = spacy.load("pt_core_news_sm")

#defining input text
text = "á árvore é verde"

#process text with NLP pipeline
doc = nlp(text)

#print tokens and their part-of-speech tags
for token in doc:
  print(token.text, token.pos_)

#por enquanto ta brabo, funcionando de boa