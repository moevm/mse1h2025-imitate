from .abstract.EffectBase import EffectBase
from .abstract.TextEffect import TextEffect


class LispEffect(EffectBase, TextEffect):
    name = 'Шепелявость'
    description = 'Заменяет все звонкие звуи на шипящие'
    input_tag = '<input type="checkbox">'

    replacements = {
        'здр': 'вдр',
        'ст': 'фт',
        'ск': 'фк',
        'с': 'ф',
        'з': 'в',
        'ш': 'ф',
        'ж': 'в',
        'ч': 'ть',
        'щ': 'сь',
    }

    def apply(self, text: str) -> str:
        for old, new in self.replacements.items():
            text = text.replace(old, new)
            text = text.replace(old[0].upper() + old[1:], new[0].upper() + new[1:])
        return text