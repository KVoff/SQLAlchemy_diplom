from fastapi import APIRouter
from app.schemas.orders import SOrderCreate
from app.service.orders_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/create", summary="Создать заказ")
def create_order(order_data: SOrderCreate):
    order = OrderService.create_order(order_data)
    return {"message": "Заказ успешно создан", "order": order}


