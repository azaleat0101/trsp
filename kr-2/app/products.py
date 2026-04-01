from typing import List, Optional
from fastapi import APIRouter, HTTPException
from .models import Product

router = APIRouter()

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99,
}
sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99,
}
sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99,
}
sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99,
}
sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99,
}

sample_products: List[Product] = [
    Product(**sample_product_1),
    Product(**sample_product_2),
    Product(**sample_product_3),
    Product(**sample_product_4),
    Product(**sample_product_5),
]


@router.get("/product/{product_id}")
def get_product(product_id: int):
    for product in sample_products:
        if product.product_id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@router.get("/products/search")
def search_products(
    keyword: str,
    category: Optional[str] = None,
    limit: int = 10,
):
    keyword_lower = keyword.lower()
    results: List[Product] = []

    for product in sample_products:
        if keyword_lower in product.name.lower():
            if category and product.category.lower() != category.lower():
                continue
            results.append(product)

    return results[:limit]