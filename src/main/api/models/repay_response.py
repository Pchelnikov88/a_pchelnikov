from src.main.api.models.base_model import BaseModel

class RepayResponse(BaseModel):
    creditId: int
    amountDeposited: float