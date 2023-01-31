from enum import Enum
from pydantic import BaseModel, validator


class PayTypeEnum(str, Enum):
    payin = "payin"
    payout = "payout"


class RequestModel(BaseModel):
    from_iban: str
    to_iban: str
    amount: str

    @validator("amount")
    def check_amount(cls, v):
        try:
            int(v)
            return v
        except ValueError as err:
            raise ValueError("Amount not a valid int number.") from err


class TransactionModel(BaseModel):
    amount: str
    wallet_id: str
    type: PayTypeEnum
    iban: str
