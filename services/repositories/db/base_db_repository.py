from abc import ABC, abstractmethod


class BaseDBRepository(ABC):

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass

    @abstractmethod
    async def update(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_by_pk(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_by_name(self, *args, **kwargs):
        pass
