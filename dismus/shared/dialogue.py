from abc import ABC, abstractmethod

__author__ = 'Flavio Ferrara'


class Utterance(ABC):
    @abstractmethod
    def serialize(self):
        raise NotImplementedError
