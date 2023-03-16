from aiohttp import ClientResponse, ClientSession

from services.repositories.api.abstract_api_repository import AbstractAPIRepository


class BaseAPIRepository(AbstractAPIRepository):
    """
    Base class for API repositories. Contain logic for sending request
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
