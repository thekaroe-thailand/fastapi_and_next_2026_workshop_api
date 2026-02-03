from .user_controller import router as user_router
from .product_controller import router as product_router

__all__ = ["user_router", "product_router"]