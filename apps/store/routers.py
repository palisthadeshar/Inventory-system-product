from rest_framework.routers import DefaultRouter
from apps.store.views import WarehouseViewset

router = DefaultRouter()

router.register('warehouse',WarehouseViewset)