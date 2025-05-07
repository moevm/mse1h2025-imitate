from graduate_imitator.apps.graduation.infrastructure.utils.config import SPECIAL_SYMBOLS


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

    # вычисление 10 слов
