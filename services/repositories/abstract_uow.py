from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    # @abstractmethod
    # def commit(self):  #(3)
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def rollback(self):  #(4)
    #     raise NotImplementedError
