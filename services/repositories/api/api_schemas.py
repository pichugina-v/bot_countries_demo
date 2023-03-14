from pydantic import BaseModel, Field


class CurrencySchema(BaseModel):
    id: str = Field(..., alias='ID')
    num_code: str = Field(..., alias='NumCode')
    char_code: str = Field(..., alias='CharCode')
    nominal: int = Field(..., alias='Nominal')
    name: str = Field(..., alias='Name')
    value: float = Field(..., alias='Value')
    previous: float = Field(..., alias='Previous')


class CurrenciesSchema(BaseModel):
    currencies: list[CurrencySchema]
