from abc import ABC, abstractmethod


class AbstractAPIRepository(ABC):
    """
    Abstract class for all API repositories
    """

    @abstractmethod
    async def _parse_response(self, *args, **kwargs):
        """
        Abstract function for parsing response
        """
        pass
