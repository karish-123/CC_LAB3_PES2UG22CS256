from dataclasses import dataclass
from typing import List, Optional, Dict
from products import dao

@dataclass
class Product:
    id: int
    name: str
    description: str
    cost: float
    qty: int = 0

    @classmethod
    def from_dict(cls, data: Dict) -> 'Product':
        """
        Create a Product instance from a dictionary.
        Handles missing or invalid data gracefully.
        """
        try:
            return cls(
                id=int(data['id']),
                name=str(data['name']),
                description=str(data['description']),
                cost=float(data['cost']),
                qty=int(data.get('qty', 0))
            )
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Invalid product data: {str(e)}")

    def to_dict(self) -> Dict:
        """Convert Product instance to dictionary for serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'cost': self.cost,
            'qty': self.qty
        }

    def validate(self) -> bool:
        """Validate product data."""
        return (
            isinstance(self.id, int) and self.id > 0 and
            isinstance(self.name, str) and len(self.name.strip()) > 0 and
            isinstance(self.description, str) and
            isinstance(self.cost, (int, float)) and self.cost >= 0 and
            isinstance(self.qty, int) and self.qty >= 0
        )

def list_products() -> List[Product]:
    """
    Retrieve all products from the database.
    Returns empty list if no products exist.
    """
    try:
        products_data = dao.list_products()
        return [Product.from_dict(product_data) 
                for product_data in products_data 
                if product_data]  # Filter out None or empty products
    except Exception as e:
        # Log error here if logging is implemented
        return []

def get_product(product_id: int) -> Optional[Product]:
    """
    Retrieve a specific product by ID.
    Returns None if product doesn't exist.
    """
    try:
        product_data = dao.get_product(product_id)
        return Product.from_dict(product_data) if product_data else None
    except Exception as e:
        # Log error here if logging is implemented
        return None

def add_product(product: Dict) -> bool:
    """
    Add a new product to the database.
    Validates product data before adding.
    Returns True if successful, False otherwise.
    """
    try:
        # Validate product data by attempting to create a Product instance
        product_instance = Product.from_dict(product)
        if not product_instance.validate():
            return False
            
        dao.add_product(product_instance.to_dict())
        return True
    except (ValueError, Exception):
        return False

def update_qty(product_id: int, qty: int) -> bool:
    """
    Update product quantity.
    Returns True if successful, False otherwise.
    """
    try:
        if not isinstance(qty, int) or qty < 0:
            raise ValueError('Quantity must be a non-negative integer')
            
        if not get_product(product_id):
            raise ValueError('Product does not exist')
            
        dao.update_qty(product_id, qty)
        return True
    except Exception:
        return False

def batch_update_qty(updates: Dict[int, int]) -> Dict[int, bool]:
    """
    Batch update quantities for multiple products.
    Returns dictionary mapping product IDs to success status.
    """
    results = {}
    for product_id, qty in updates.items():
        results[product_id] = update_qty(product_id, qty)
    return results