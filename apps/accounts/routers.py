from rest_framework.routers import DefaultRouter
from apps.accounts.views import (
    UserViewSet,
    CustomerViewSet,
    BillerViewSet,
    SupplierViewSet,
    ForgotPasswordView,
)

router = DefaultRouter()
router.register("user", UserViewSet)
router.register("customer",CustomerViewSet)
router.register("biller",BillerViewSet)
router.register("supplier",SupplierViewSet)
router.register("forgot-password", ForgotPasswordView, basename="forgot-password")
