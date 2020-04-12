from abc import ABC, abstractmethod


class IModel(ABC):

    @abstractmethod
    def solve(self):
        pass

    @abstractmethod
    def get_json(self):
        pass
