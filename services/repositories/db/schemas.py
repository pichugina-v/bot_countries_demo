from pydantic import BaseModel


class CurrencyCodesSchema(BaseModel):
    """
    Pydantic schema for CountryDBRepository. Using for getting all currecny codes for contcrete country.
    """
    currency_codes: list[str]


class LanguageNamesSchema(BaseModel):
    """
    Pydantic schema for CountryDBRepository. Using for getting all languge names for contcrete country.
    """
    languages: list[str]
