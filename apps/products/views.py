from rest_framework.viewsets import ModelViewSet
from apps.products.models import (
    Brand,
    Category,
    Product,
    Unit,
    Barcode,
    Purchase,
    Sales,
    PurchaseInvoice,
    SalesInvoice,
    Adjustment
)
from apps.products.serializers import (
    BrandSerializers,
    CategorySerializer,
    ProductSerializer,
    GETProductSerializer,
    UnitSerializer,
    GetCategorySeralizer,
    GetUnitSeralizer,
    GetBrandSeralizer,
    BarcodeSerializer,
    GetBarcodeSerializer,
    PurchaseSerializer,
    SalesSerializer,
    GetPurachseSerializer,
    PurchaseInvoiceSerializer,
    AdjustmentSerializer,
    GetAdjustmentSeralizer,
    GetSalesSerializer,
    GetPurchaseInvoiceSerializer,
    SalesInvoiceSerializer,
    GetSalesInvoiceSerializer
)
from apps.products.pagination import Pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
# from utils.permissions import SupplierPermssion
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
import barcode
from barcode.writer import ImageWriter
import uuid
import os
from django.db.models import Sum


# Create your views here.
class MyPagination(ModelViewSet):
    pagination_class = Pagination


class BrandViewSet(MyPagination):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers
    http_method_names = ["get", "post", "put", "delete"]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["brand_name"]

    def create(self, request, *args, **kwargs):
        serializers = BrandSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(created_by=request.user, modified_by=None)
        return Response(serializers.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializers = BrandSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(modified_by=request.user)
        return Response(serializers.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetBrandSeralizer
        return super().get_serializer_class()


class CategoryViewSet(MyPagination):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ["get", "post", "delete"]

    def create(self, request, *args, **kwargs):
        serializers = CategorySerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(created_by=request.user, modified_by=None)
        return Response(serializers.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetCategorySeralizer
        return super().get_serializer_class()


class UnitViewSet(ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    # permission_classes = [IsUserAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["=short_name"]
    ordering_fields = ["short_name"]

    def create(self, request, *args, **kwargs):
        serializers = UnitSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(created_by=request.user)
        return Response(serializers.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetUnitSeralizer
        return super().get_serializer_class()



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["created_by"]
    permission_classes_by_action = {
        "list": [AllowAny],
        "retrieve": [IsAuthenticated],
        # "create": [IsAdminUser | SupplierPermssion],
        # "update": [IsAuthenticated | SupplierPermssion],
    }

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except:
            return [permission() for permission in self.permission_classes]

    # def create_or_update_warehouse(self, warehouses):
    #     warehouse_ids = []
    #     # print(warehouses)
    #     for warehouse in warehouses:
    #         warehouse_instance, created = Warehouse.objects.update_or_create(
    #             id=warehouse.get("id"), defaults=warehouse
    #         )
    #         warehouse_ids.append(warehouse_instance.id)
    #     return warehouse_ids

    # def partial_update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     warehouse_data = request.data.pop("warehouse")
    #     warehouse = self.create_or_update_warehouse(warehouse_data)
    #     instance.warehouse.set(warehouse)
    #     serializer = ProductSerializer(instance)
    #     return Response(serializer.data)

    # def partial_update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     warehouse_data = request.data.pop("warehouse")
    #     warehouse_ids_list = []
    #     for warehouse in warehouse_data:
    #         warehouse_instance = Warehouse.objects.get(id = warehouse)

    #         warehouse_ids_list.append(warehouse_instance.id)
    #     instance.warehouse.set(warehouse_ids_list)
    #     serializer = ProductSerializer(instance)

    #     return Response({"updated data" : serializer.data})

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GETProductSerializer
        return super().get_serializer_class()


class BarcodeViewset(ModelViewSet):
    queryset = Barcode.objects.all()
    serializer_class = BarcodeSerializer

    def create(self, request, *args, **kwargs):
        product_information = request.data.get("information")
        get_current_product = Product.objects.get(id=product_information)
        get_current_product_code = get_current_product.product_code
        if not get_current_product_code:
            # print(product_infromation.product_code)
            return Response(
                {"error": "Product code is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        barcode_class = barcode.get_barcode_class("code128")
        code = barcode_class(get_current_product_code, writer=ImageWriter())

        unique_filename = f"barcode_{uuid.uuid4()}"

        directory_path = "barcode-image/"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        barcode_image = code.save(f"barcode-image/{unique_filename}")

        serializer = BarcodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(barcode_image=barcode_image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetBarcodeSerializer
        return super().get_serializer_class()


class AdjustmentViewset(ModelViewSet):
    queryset = Adjustment.objects.all()
    serializer_class = AdjustmentSerializer

    def create(self, request):
        serializer = AdjustmentSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop('quantity')
        adjustment = Adjustment.objects.create(**serializer.validated_data)
        serializer = AdjustmentSerializer(adjustment)
        return Response({"data" : serializer.data}) 
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetAdjustmentSeralizer
        return super().get_serializer_class()
    
class PurchaseViewSet(ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetPurachseSerializer
        return super().get_serializer_class()


class SalesViewSet(ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetSalesSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        data = request.data
        # import pdb;pdb.set_trace()
        serializer = SalesSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        for product_data in data["product"]:                
            get_product_by_id = Product.objects.get(id=product_data)
            required_quantity = get_product_by_id.stock_alert

            if data['quantity'] < required_quantity:
                return Response({'errors' : 'total quantiy is greater than required quantity.'})
            else:
                pass
        
        return Response({"data": serializer.data, "message": "success sales"},status=status.HTTP_200_OK)

class PurchaseInvoiceViewSet(ModelViewSet):
    queryset = PurchaseInvoice.objects.all()
    serializer_class = PurchaseInvoiceSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetPurchaseInvoiceSerializer
        return super().get_serializer_class()
    
class SalesInvoiceViewSet(ModelViewSet):
    queryset = SalesInvoice.objects.all()
    serializer_class = SalesInvoiceSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetSalesInvoiceSerializer
        return super().get_serializer_class()


    