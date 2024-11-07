from app.models.products import Product
from app.service.base import BaseService


class ProductService(BaseService):
    model = Product
