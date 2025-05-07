from graduate_imitator.apps.graduation.infrastructure.utils.config import SPECIAL_SYMBOLS
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def clear_text(text):
    for item in SPECIAL_SYMBOLS:
        text = text.replace(item, "")
    return text.strip()


def delete_trash_words(text):

    # удаление треш слов

    return text


def get_10_keywords(text):
    new_text = text[::]
    for i in range(len(new_text)):
        new_text[i] = delete_trash_words(new_text[i])

    vectorizer = TfidfVectorizer()

    # Преобразуем документы в матрицу TF-IDF
    tfidf_matrix = vectorizer.fit_transform(new_text)

    # Получаем имена всех слов
    feature_names = vectorizer.get_feature_names_out()

    # Суммируем значения TF-IDF по всем документам
    tfidf_sum = np.sum(tfidf_matrix.toarray(), axis=0)

    # Получаем индексы 10 ключевых слов с наибольшими значениями TF-IDF
    top_n = 10
    top_n_indices = np.argsort(tfidf_sum)[-top_n:][::-1]

    # Получаем ключевые слова
    top_n_keywords = [feature_names[i] for i in top_n_indices]

    return top_n_keywords
