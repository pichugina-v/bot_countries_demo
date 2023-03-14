import json
from http import HTTPStatus

from aiohttp import ClientResponse

from services.currency_code import CurrenciesCode
from services.repositories.api.api_schemas import CurrenciesSchema, CurrencySchema
from services.repositories.api.api_settings import CURRENCY_INFO_URL
from services.repositories.api.base_api_repository import BaseAPIRepository


class CurrencyAPIRepository(BaseAPIRepository):
    """
    This class is a repository for making requests in currency API.
    """

    async def get_rate(self, char_code: CurrenciesCode) -> float | None:
        """
        Return current currency rate for received currency code.

        :param char_code: currency code like "USD" or "EUR"

        :return: currency rate if it exists
        """
        response = await self._send_request(url=CURRENCY_INFO_URL)
        if response.status == HTTPStatus.OK:
            data = await self._parse_response(response)
            for currency_data in data.currencies:
                if currency_data.char_code == char_code.value:
                    return currency_data.value
        return None

    async def _parse_response(self, response: ClientResponse) -> CurrenciesSchema:
        """
        This function parse response.

        :param response: response from aiohttp

        :return: parsed response
        """

        data_cbr = json.loads(await response.read())
        row_currencies = data_cbr['Valute']
        parsed_currencies = []
        for currency_code in row_currencies:
            parsed_currencies.append(CurrencySchema.parse_obj(row_currencies[currency_code]))

        return CurrenciesSchema(currencies=parsed_currencies)
