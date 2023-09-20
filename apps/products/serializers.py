from rest_framework import serializers
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
    Adjustment,
)
from apps.accounts.serializers import (
    UserSerializer,
    SupplierSerializer,
    BillerSerializer,
    CustomerSerializer,
)
from apps.store.serializers import WarehouseSerializer
from apps.store.models import Warehouse
from rest_framework.response import Response


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "brand_name",
            "brand_image",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "main_category", "sub_category")

    def validate(self, data):
        if data["sub_category"] == data["main_category"]:
            raise serializers.ValidationError(
                {"sub_category": "Sub category cannot be same as main category."}
            )
        return data


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ("unit_name", "short_name")


class ProductSerializer(serializers.ModelSerializer):
    # warehouse = WarehouseSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "product_name",
            "product_type",
            "category",
            "product_code",
            "brand",
            "barcode",
            "product_unit",
            "product_price",
            "expense",
            "unit_price",
            "product_tax",
            "tax_method",
            "discount",
            "stock_alert",
            "product_image",
            "featured",
            "warehouse",
            "price_difference_in_warehouse",
            "has_expiry_date",
            "add_promotional_sale",
            "has_multi_variant",
            "has_imie_code",
        )

    def create(self, validated_data):
        warehouse_data = validated_data.pop("warehouse", [])

        product = Product.objects.create(**validated_data)
        for warehouse_info in warehouse_data:
            warehouse_id = warehouse_info.id

            try:
                warehouse_obj = Warehouse.objects.get(id=warehouse_id)
                product.warehouse.add(warehouse_obj)
            except Warehouse.DoesNotExist:
                return Response({"message": "no such warehouse exists."})

        return product


class BarcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barcode
        fields = ("id", "information", "papersize")


class AdjustmentSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(write_only=True)

    class Meta:
        model = Adjustment
        fields = ("id", "quantity", "warehouse", "product", "type")

    def validate(self, data):
        product = data.get("product")
        type = data.get("type")
        quantity = data.get("quantity")
        if type == "Substraction" and product.stock_alert < quantity:
            raise serializers.ValidationError(
                {product.product_name: "Stock is less than quantity to be substracted."}
            )
        elif type == "Addition":
            product.stock_alert += int(quantity)
        else:
            product.stock_alert -= int(quantity)
        product.save()

        return data


class GETProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializers()
    category = CategorySerializer()
    product_unit = UnitSerializer()
    created_by = UserSerializer()
    modified_by = UserSerializer()
    user = UserSerializer()
    warehouse = WarehouseSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class GetBarcodeSerializer(serializers.ModelSerializer):
    information = ProductSerializer()

    class Meta:
        model = Barcode
        fields = "__all__"


class GetCategorySeralizer(serializers.ModelSerializer):
    created_by = UserSerializer()
    modified_by = UserSerializer()

    class Meta:
        model = Category
        fields = (
            "created_by",
            "modified_by",
            "main_category",
            "sub_category",
        )


class GetUnitSeralizer(serializers.ModelSerializer):
    created_by = UserSerializer()
    modified_by = UserSerializer()

    class Meta:
        model = Unit
        fields = ("created_by", "modified_by", "unit_name", "short_name")


class GetBrandSeralizer(serializers.ModelSerializer):
    created_by = UserSerializer()
    modified_by = UserSerializer()

    class Meta:
        model = Brand
        fields = (
            "created_by",
            "modified_by",
            "brand_name",
            "brand_image",
        )


class GetAdjustmentSeralizer(serializers.ModelSerializer):
    product = ProductSerializer()
    warehouse = WarehouseSerializer()

    class Meta:
        model = Adjustment
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = (
            "id",
            "warehouse",
            "supplier",
            "product",
            "order_tax",
            "order_discount",
            "shipping",
            "sales_status",
            "purchase_note",
        )


class GetPurachseSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer()
    supplier = SupplierSerializer()
    product = ProductSerializer(many=True)

    class Meta:
        model = Purchase
        fields = (
            "warehouse",
            "supplier",
            "product",
            "order_tax",
            "order_discount",
            "shipping",
            "sales_status",
            "purchase_note",
        )


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = (
            "customer",
            "warehouse",
            "biller",
            "product",
            "sales_tax",
            "discount",
            "shipping",
            "sales_status",
            "payment_status",
            "sales_image",
            "sales_note",
            "staff_remark",
        )


class GetSalesSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer()
    biller = BillerSerializer()
    customer = CustomerSerializer()
    product = ProductSerializer(many=True)

    class Meta:
        model = Sales
        fields = (
            "customer",
            "warehouse",
            "biller",
            "product",
            "sales_tax",
            "discount",
            "shipping",
            "sales_status",
            "payment_status",
            "sales_image",
            "sales_note",
            "staff_remark",
        )


class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseInvoice
        fields = ("id", "warehouse", "supplier", "purchases")


class GetPurchaseInvoiceSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer()
    supplier = SupplierSerializer()
    purchases = PurchaseSerializer()

    class Meta:
        model = PurchaseInvoice
        fields = "__all__"

class SalesInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInvoice
        fields = ("id", "warehouse", "supplier", "sales")


class GetSalesInvoiceSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer()
    supplier = SupplierSerializer()
    sales = SalesSerializer()

    class Meta:
        model = SalesInvoice
        fields = "__all__"
