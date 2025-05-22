from abc import ABC, abstractmethod


class EffectBase(ABC):
    name: str
    description: str

    @abstractmethod
    def apply(self):
        pass

    def __str__(self):
        return f'{self.name}\n{self.description}'