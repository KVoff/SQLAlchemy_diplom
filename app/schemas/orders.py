from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class SOrderItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int


class SOrderCreate(BaseModel):
    buyer_id: int
    items: List[SOrderItem]


class SOrder(BaseModel):
    order_id: int
    created_at: datetime = Field(
        ...,
        description="Дата создания заказа в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС")
    price: float = Field(
        ...,
        description="Общая стоимость заказа")
    order_items: List[SOrderItem] = Field(
        ...,
        description="Состав заказа")
