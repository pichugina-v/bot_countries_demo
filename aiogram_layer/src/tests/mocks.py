from collections import deque
from typing import TYPE_CHECKING, AsyncGenerator, Deque, Optional, Type

from aiogram import Bot
from aiogram.client.session.base import BaseSession
from aiogram.methods import TelegramMethod
from aiogram.methods.base import Response, TelegramType
from aiogram.types import UNSET, ResponseParameters, User


class MockedSession(BaseSession):
    def __init__(self):
        super().__init__()
        self.responses: Deque[Response[TelegramType]] = deque()
        self.requests: Deque[TelegramMethod[TelegramType]] = deque()
        self.closed = True

    def add_result(self, response: Response[TelegramType]) -> Response[TelegramType]:
        self.responses.append(response)
        return response

    def get_request(self) -> TelegramMethod[TelegramType]:
        return self.requests.pop()

    async def close(self):
        self.closed = True

    async def make_request(
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
        timeout: int | None = UNSET,
    ) -> TelegramType:
        self.closed = False
        # self.requests.append(method)
        # response: Response[TelegramType] = self.responses.pop()
        # self.check_response(
        #     method=method, status_code=response.error_code, content=response.json()
        # )
        # return response.result  # type: ignore
        return method

    async def stream_content(
        self,
        url: str,
        timeout: int,
        chunk_size: int,
        raise_for_status: bool,
    ) -> AsyncGenerator[bytes, None]:  # pragma: no cover
        yield b''


class MockedBot(Bot):
    if TYPE_CHECKING:
        session: MockedSession

    def __init__(self, **kwargs):
        super().__init__(
            kwargs.pop('token', '42:TEST'), session=MockedSession(), **kwargs
        )
        self._me = User(
            id=self.id,
            is_bot=True,
            first_name='FirstName',
            last_name='LastName',
            username='tbot',
            language_code='uk-UA',
        )

    def add_result_for(
        self,
        method: type[TelegramMethod[TelegramType]],
        ok: bool,
        result: TelegramType = None,
        description: str | None = None,
        error_code: int = 200,
        migrate_to_chat_id: int | None = None,
        retry_after: int | None = None,
    ) -> Response[TelegramType]:
        response = Response[method.__returning__](  # type: ignore
            ok=ok,
            result=result,
            description=description,
            error_code=error_code,
            parameters=ResponseParameters(
                migrate_to_chat_id=migrate_to_chat_id,
                retry_after=retry_after,
            ),
        )
        self.session.add_result(response)
        return response

    def get_request(self) -> TelegramMethod[TelegramType]:
        return self.session.get_request()