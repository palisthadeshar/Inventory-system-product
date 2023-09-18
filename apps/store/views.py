from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from apps.store.models import Warehouse
from apps.store.serializers import WarehouseSerializer

class WarehouseViewset(ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    http_method_names = ['get','post','put','delete'] 