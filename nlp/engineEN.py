import spacy

#loading ENG language model
enMODEL = spacy.load("en_core_web_sm")

#loading PT language model
# nlpPT = spacy.load("pt_core_news_sm")

#defining input text
# text = "A parede é azul"

#process text with NLP pipeline
# doc = nlpEN(text)

def extract_entities(message):
  doc = enMODEL(message)
  entities = [ent.text for ent in doc.ents]
  return entities

#print tokens and their part-of-speech tags
# for token in doc:
#   print(token.text, token.pos_)