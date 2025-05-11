import spacy

SPECIAL_SYMBOLS = ['\t', '\n', '\r']
RUSSIAN_NLP_MODEL = nlp = spacy.load("ru_core_news_sm")
