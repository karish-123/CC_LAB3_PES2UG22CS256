from dataclasses import dataclass
from typing import List, Optional
import json
from products import Product, get_product
from cart import dao

@dataclass
class Cart:
    id: int
    username: str
    contents: List[Product]
    cost: float

    @classmethod
    def from_dict(cls, data: dict) -> 'Cart':
        """Create a Cart instance from a dictionary."""
        return cls(
            id=data['id'],
            username=data['username'],
            contents=data['contents'],
            cost=data['cost']
        )

    def to_dict(self) -> dict:
        """Convert Cart instance to dictionary for serialization."""
        return {
            'id': self.id,
            'username': self.username,
            'contents': [product.id for product in self.contents],
            'cost': self.cost
        }

def get_cart(username: str) -> List[Product]:
    """
    Retrieve and return the cart contents for a given username.
    Returns empty list if no cart exists.
    """
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []
    
    # Extract all product IDs from cart details
    product_ids = set()
    for detail in cart_details:
        try:
            contents = json.loads(detail['contents'])
            product_ids.update(contents)
        except (json.JSONDecodeError, TypeError, KeyError):
            continue
    
    # Batch fetch all products at once
    products = []
    for product_id in product_ids:
        product = get_product(product_id)
        if product:
            products.append(product)
    
    return products

def add_to_cart(username: str, product_id: int) -> bool:
    """
    Add a product to cart. Returns True if successful, False otherwise.
    """
    try:
        dao.add_to_cart(username, product_id)
        return True
    except Exception:
        return False

def remove_from_cart(username: str, product_id: int) -> bool:
    """
    Remove a product from cart. Returns True if successful, False otherwise.
    """
    try:
        dao.remove_from_cart(username, product_id)
        return True
    except Exception:
        return False

def delete_cart(username: str) -> bool:
    """
    Delete entire cart for a user. Returns True if successful, False otherwise.
    """
    try:
        dao.delete_cart(username)
        return True
    except Exception:
        return False