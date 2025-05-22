from .abstract.EffectBase import EffectBase
from .abstract.TextEffect import TextEffect


class RLispEffect(EffectBase, TextEffect):
    name = 'Картавость'
    description = 'Заменяет все `р` на `л`'
    input_tag = '<input type="checkbox">'

    replacements = {
        'р': 'л',
        'Р': 'Л'
    }

    def apply(self, text: str) -> str:
        for old, new in self.replacements.items():
            text = text.replace(old, new)
            text = text.replace(old[0].upper() + old[1:], new[0].upper() + new[1:])
        return text