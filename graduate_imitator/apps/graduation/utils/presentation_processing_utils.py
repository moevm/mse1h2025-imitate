from graduate_imitator.apps.graduation.infrastructure.utils.config import SPECIAL_SYMBOLS


def clear_text(text):
    new_text = text[::]
    for i in range(len(new_text)):
        item = new_text[i]
        for jtem in SPECIAL_SYMBOLS:
            item = item.replace(jtem, "")
        new_text[i] = item
    return new_text


def delete_trash_words(text):
    pass


def get_10_most_popular_words(text):
    text = clear_text(text)
