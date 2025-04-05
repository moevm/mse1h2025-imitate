from typing import List
from mse1h2025_imitate.graduation_imitator.configs.presentation_config import SPECIAL_SYMBOLS


def deleteAll(string: str, symbols: List) -> str:
    ''' Function to delete all symbols from string
    Args:
        string: str - string
        symbols: list - symbols (to be deleted) sequence
    Returns:
        string: str - string without symbols from `symbols` list
    '''
    for symbol in symbols:
        string = string.replace(symbol, '')
    return string

def deleteSpecialSymbolsFromOutput(func):
    ''' Decorator to delete config.SPECIAL_SYMBOLS from function output'''
    def wrapper(*args, **kwargs):
        return deleteAll(func(*args, **kwargs).strip(), SPECIAL_SYMBOLS)
    return wrapper