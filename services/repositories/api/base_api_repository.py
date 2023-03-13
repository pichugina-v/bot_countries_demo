from abc import ABC, abstractmethod

from aiohttp import ClientResponse, ClientSession


class BaseAPIRepository(ABC):
    """
    Abstract class for API repositories
    """

    @staticmethod
    async def _send_request(url: str) -> ClientResponse:
        """
        Send GET response

        :param url: API url address

        :return: response from API
        """
        async with ClientSession() as session:
            resp = await session.get(url)
        return resp

    @abstractmethod
    async def _parse_response(self, response: ClientResponse):
        """
        Abstract function for parsing response

        :param response: response from API

        :return: None
        """
