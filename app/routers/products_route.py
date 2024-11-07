from typing import List

from fastapi import APIRouter, HTTPException, Depends

from app.schemas.request import RbProduct
from app.service.products_service import ProductService
from app.schemas.products import SProductAdd, SProductUpdate, SProduct

router = APIRouter(prefix='/products', tags=['Список товаров'])


@router.get("/", summary="Все продукты", response_model_exclude_none=True)
def get_all_products(request_body: RbProduct = Depends()) -> list[SProduct]:
    return ProductService.find_all(**request_body.to_dict())

@router.post("/add/")
def add_product(product: SProductAdd) -> dict:
    check = ProductService.add(**product.model_dump())
    if check:
        return {"message": "Товар успешно добавлен!", "product": product}
    else:
        return {"message": "Ошибка при добавлении товара!"}


@router.put("/update_product/")
def update_product(product: SProductUpdate) -> dict:
    # Найдите продукт по имени
    existing_product = ProductService.get(name=product.name)
    if not existing_product:
        return {"message": "Продукт не найден!"}

        # Извлекаем только переданные значения
    update_values = product.model_dump(exclude_unset=True)
    if not update_values:
        return {"message": "Нет данных для обновления."}

    # Обновляем продукт
    updated_count = ProductService.update(filter_by={"name": product.name},
                                          **update_values)

    if updated_count:
        return {
            "message": "Продукт успешно обновлен!",
            "product": {**existing_product.to_dict(), **update_values}
        }
    else:
        return {"message": "Ошибка при обновлении продукта!"}


@router.delete("/delete/{product_id}")
def delete_product(product_id: int) -> dict:
    check = ProductService.delete(id=product_id)
    if check:
        return {"message": f"Продукт с ID {product_id} удален!"}
    else:
        return {"message": "Ошибка при удалении продукта!"}
