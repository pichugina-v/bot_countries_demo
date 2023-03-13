import json

from aiohttp import ClientResponse

from services.currency_code import CurrenciesCode
from services.repositories.api.base_api_repository import BaseAPIRepository


class CurrencyAPIRepository(BaseAPIRepository):
    """
    This class is a repository for making requests in currency API.
    """

    async def get_rate(self, currency_code: CurrenciesCode) -> float:
        """
        Return current currency rate for received currency code.

        :param currency_code: currency code like "USD" or "EUR"
        :type: CurrenciesCode

        :return: currency rate
        :rtype: float
        """

        response = await self._send_request(url='https://www.cbr-xml-daily.ru/daily_json.js')
        if response.status == 200:
            data_cbr = await self._parse_response(response)
            currencies = data_cbr.get('Valute')
            currency_info = currencies.get(currency_code.value)
            rate = currency_info.get('Value')
            return rate

    async def _parse_response(self, response: ClientResponse) -> dict:
        """
        This function parse response.

        :param response: response from aiohttp
        :type: ClientResponse

        :return: parsed response
        :rtype: float
        """

        data_cbr = json.loads(await response.read())
        return data_cbr
