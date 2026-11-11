from pydantic import Field
from typing import Annotated
from src.main.api.models.base_model import BaseModel
from src.main.api.generators.creation_rule import CreationRule


class DepositRequest(BaseModel):
    accountId: int

    # Валидация: от 1000 до 9000
    amount: Annotated[
        float,
        Field(ge=1000, le=9000),
        CreationRule(regex=r"^[1-8][0-9]{3}$|^9000$")
    ]