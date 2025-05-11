from graduate_imitator.apps.graduation.infrastructure.utils.config import SPECIAL_SYMBOLS, RUSSIAN_NLP_MODEL
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy


def clear_text(text):
    for item in SPECIAL_SYMBOLS:
        text = text.replace(item, "")
    return text.strip()


def delete_trash_words(text):
    doc = RUSSIAN_NLP_MODEL(text)
    cleaned_words = []
    for token in doc:
        if not token.is_stop and not token.is_punct:
            cleaned_words.append(token.lemma_)
    return " ".join(cleaned_words)


def get_10_keywords(text):
    new_text = text[::]
    for i in range(len(new_text)):
        new_text[i] = delete_trash_words(new_text[i])
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(new_text)
        feature_names = vectorizer.get_feature_names_out()
        tfidf_sum = np.sum(tfidf_matrix.toarray(), axis=0)
        top_n = 10
        top_n_indices = np.argsort(tfidf_sum)[-top_n:][::-1]
        top_n_keywords = [feature_names[i] for i in top_n_indices]
        return top_n_keywords
    except ValueError:
        return ["Presentation is empty (TfidfVectorizer error)"]
