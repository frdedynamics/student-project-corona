from abc import ABC, abstractmethod, abstractproperty


class IModel(ABC):

    @property
    @abstractmethod
    def LOCALS(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def solve(self):
        pass

    @abstractmethod
    def get_json(self) -> str:
        pass
