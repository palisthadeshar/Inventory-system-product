from rest_framework.routers import DefaultRouter
from apps.products.views import (
    ProductViewSet,
    BrandViewSet,
    CategoryViewSet,
    UnitViewSet,
)

router = DefaultRouter()
router.register("product", ProductViewSet)
router.register("brand", BrandViewSet)
router.register("cateogry", CategoryViewSet)
router.register("unit", UnitViewSet)
