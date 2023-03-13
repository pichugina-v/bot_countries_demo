from aiohttp import ClientResponse, ClientSession


class BaseAPIRepository:

    @staticmethod
    async def _send_request(url: str) -> ClientResponse:
        async with ClientSession() as session:
            resp = await session.get(url)
        return resp

    async def _parse_response(self, response: ClientResponse):
        raise NotImplementedError('Требуется реализовать метод парсинга ответа от АПИ')