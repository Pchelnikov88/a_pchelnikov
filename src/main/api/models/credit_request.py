from pydantic import Field
from typing import Annotated
from src.main.api.models.base_model import BaseModel
from src.main.api.generators.creation_rule import CreationRule


class CreditRequest(BaseModel):
    accountId: int

    # Валидация: от 5000 до 15000
    amount: Annotated[
        float,
        Field(ge=5000, le=15000),
        CreationRule(regex=r"^[5-9][0-9]{3}$|^1[0-4][0-9]{3}$|^15000$")
    ]
    termMonths: int