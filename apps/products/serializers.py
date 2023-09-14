from rest_framework import serializers
from apps.products.models import Brand, Category, Product, Unit, Barcode
from apps.accounts.serializers import UserSerializer
from apps.store.serializers import WarehouseSerializer
from apps.store.models import Warehouse


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
    warehouse = WarehouseSerializer(many=True, read_only=False)

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
        warehouses_data = validated_data.pop("warehouse")
        product = Product.objects.create(**validated_data)

        for warehouse_data in warehouses_data:
            warehouses, created = Warehouse.objects.get_or_create(**warehouse_data)
            product.warehouse.add(warehouses)

        return product

    def update(self, instance, validated_data):
        warehouse_ids = validated_data.pop('warehouse', None)
        import pdb
        pdb.set_trace()
        if warehouse_ids:
            product = Product.objects.get(id=validated_data.get("id"))
            instance.warehouse.add(warehouse_ids)

        return super().update(instance, validated_data)


class BarcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barcode
        fields = ("information", "papersize")


class GETProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializers()
    category = CategorySerializer()
    product_unit = UnitSerializer()
    created_by = UserSerializer()
    modified_by = UserSerializer()
    user = UserSerializer()

    class Meta:
        model = Product
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
