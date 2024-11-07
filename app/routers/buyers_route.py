from fastapi import APIRouter, Depends, HTTPException

from app.models import Buyer
from app.schemas.buyer import SBuyer, SBuyerAdd
from app.schemas.orders import SOrder
from app.schemas.request import RbBuyer
from app.service.buyers_service import BuyerService
from app.service.orders_service import OrderService

router = APIRouter(prefix='/buyers', tags=['Покупатели'])


@router.get("/", summary="Все покупатели", response_model_exclude_none=True)
def get_all_buyers(request_body: RbBuyer = Depends()) -> list[SBuyer]:
    return BuyerService.find_all(**request_body.to_dict())


@router.get("/{id}", summary="Получить одного покупателя по id")
def get_buyer_by_id(buyer_id: int) -> SBuyer | dict:
    rez = BuyerService.find_full_data(buyer_id)
    if rez is None:
        return {'message': f'Покупатель с ID {buyer_id} не найден!'}
    return rez


@router.get("/buyer/orders", summary="Получить заказы покупателя")
def get_buyer_orders(buyer: RbBuyer = Depends()) -> list[SOrder]:
    orders = OrderService.find_orders_by_buyer(buyer)
    if not orders:
        raise HTTPException(status_code=404, detail="Заказы не найдены")
    return [order.to_dict() for order in orders]

@router.post("/add/")
def add_buyer(buyer: SBuyerAdd) -> dict:
    check = BuyerService.add(**buyer.model_dump())
    if check:
        return {"message": "Покупатель успешно добавлен!", "buyer": buyer}
    else:
        return {"message": "Ошибка при добавлении покупателя!"}
