from rest_framework.routers import DefaultRouter
from apps.products.views import (
    ProductViewSet,
    BrandViewSet,
    CategoryViewSet,
    UnitViewSet,
    BarcodeViewset,
    PurchaseViewSet,
    SalesViewSet,
    PurchaseInvoiceViewSet,
    AdjustmentViewset,
    SalesInvoiceViewSet,

)

router = DefaultRouter()
router.register("product", ProductViewSet)
router.register("brand", BrandViewSet)
router.register("cateogry", CategoryViewSet)
router.register("unit", UnitViewSet)
router.register("barcode",BarcodeViewset)
router.register("purchase",PurchaseViewSet)
router.register("sales",SalesViewSet)
router.register("purchase-invoice",PurchaseInvoiceViewSet)
router.register("adjustment",AdjustmentViewset)
router.register("sales-invoice",SalesInvoiceViewSet) 
