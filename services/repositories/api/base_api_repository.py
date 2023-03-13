from aiohttp import ClientResponse, ClientSession


class BaseAPIRepository:
    """
    Abstract class for API repositories
    """

    @staticmethod
    async def _send_request(url: str) -> ClientResponse:
        """
        Send GET response

        :param url: url address
        :type: str

        :return: response from API
        :rtype: ClientResponse
        """
        async with ClientSession() as session:
            resp = await session.get(url)
        return resp

    async def _parse_response(self, response: ClientResponse):
        """
        Abstract function for parsing response

        :param response: response from API
        :type: ClientResponse

        :return: None
        """
        raise NotImplementedError('Response parsing is not implemented')
