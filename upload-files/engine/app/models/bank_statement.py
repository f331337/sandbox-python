from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from decimal import Decimal


class Transaction(BaseModel):
    transaction_id: str = Field(alias="TransactionId")
    provider_transaction_id: str = Field(alias="ProviderTransactionId")
    creation_date: datetime = Field(alias="CreationDate")
    last_updated: datetime = Field(alias="LastUpdated")
    username: str = Field(alias="Username")
    transaction_type: str = Field(alias="TransactionType")
    business_type: str | None = Field(default=None, alias="BusinessType")
    currency: str = Field(alias="Currency")
    amount: Decimal = Field(alias="Amount")
    payment_method: str = Field(alias="PaymentMethod")
    transaction_status: str = Field(alias="TransactionStatus")
    action_required: str | None = Field(default=None, alias="ActionRequired")
    brand: str = Field(alias="Brand")
    product: str = Field(alias="Product")
    provider: str = Field(alias="Provider")
    action: str | None = Field(default=None, alias="Action")
    payment_instrument_account_reference: str | None = Field(default=None, alias="PaymentInstrumentAccountReference")

    @field_validator("creation_date", "last_updated", mode="before")
    def parse_custom_datetime(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, "%m/%d/%Y %H:%M")
        return v
