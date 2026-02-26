
from dataclasses import dataclass

@dataclass
class CheckResponce:
    '''Represents a check databace responce.'''
    message: str
    accounts: list[int]

