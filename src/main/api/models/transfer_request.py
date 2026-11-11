from pydantic import Field
from typing import Annotated
from src.main.api.models.base_model import BaseModel
from src.main.api.generators.creation_rule import CreationRule


class TransferRequest(BaseModel):
    fromAccountId: int
    toAccountId: int
    # Валидация: от 1000 до 9000
    amount: Annotated[
        float,
        Field(ge=500, le=10000),
            # Генератор создает числа от 1000 до 8999, или ровно 10000
        CreationRule(regex=r"^5[0-9]{2}$|^10000$")
    ]