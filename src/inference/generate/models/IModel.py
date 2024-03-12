from abc import ABC, abstractmethod

class IModel(ABC):
    @abstractmethod
    async def run(self):
        pass