from pydantic import BaseModel
from typing import Literal


class currency_conversion(BaseModel):
    amount =float
    from_currency= Literal['USD','EGP']
    to_currency = Literal['USD','EGP']

class invoice_item(BaseModel):
    name = str
    price =float

class invoice_schema(BaseModel):
    customer_name: str
    items =list[invoice_item]    