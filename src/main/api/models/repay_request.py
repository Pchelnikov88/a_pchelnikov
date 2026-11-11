from src.main.api.models.base_model import BaseModel

class RepayRequest(BaseModel):
    creditId: int
    accountId: int
    amount: float