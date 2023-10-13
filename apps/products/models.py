from django.db import models
from apps.products.constant import (
    PRODUCT_TYPE_CHOICES,
    PRODUCT_TAX,
    TAX_METHOD,
    BARCODE_PAPER_SIZE,
    SALE_STATUS,
    ORDER_TAX,
    ADJUSTMENT_TYPE
)
from utils.models import CommonInfo
from apps.store.models import Warehouse
from apps.accounts.models import User, Customer, Supplier, Biller
from utils.threads import get_request


# Create your models here.
class Brand(CommonInfo):
    """
    Represents a brand with a name and optional image.

    This model represents a brand entity in the system, which can have a name
    and an optional image associated with it.

    Attributes:
        brand_name (str): The name of the brand (up to 30 characters).
        brand_image (ImageField): An optional image representing the brand's logo or image.

    Inherited Attributes:
        - id (AutoField): The primary key for the brand.
        - created_at (DateTimeField): The date and time when the brand was created.
        - updated_at (DateTimeField): The date and time when the brand was last updated.

    Methods:
        __str__(): Returns a human-readable string representation of the brand.

    """
    brand_name = models.CharField(max_length=30)
    brand_image = models.ImageField(upload_to="profile/", blank=True, null=True)

    def __str__(self):
        """
        Returns a human-readable string representation of the brand.

        Returns:
            str: A string representing the brand, typically the brand name.
        """
        return self.brand_name



class Category(CommonInfo):
    """
    Represents a category with main and subcategories.

    This model represents a category that can be used to classify various items
    into main categories and subcategories.

    Attributes:
        main_category (str): The main category name (up to 30 characters).
        sub_category (str): The subcategory name (up to 30 characters).

    Inherited Attributes:
        - id (AutoField): The primary key for the category.
        - created_at (DateTimeField): The date and time when the category was created.
        - updated_at (DateTimeField): The date and time when the category was last updated.

    Methods:
        __str__(): Returns a human-readable string representation of the category.

    """

    main_category = models.CharField(max_length=30)
    sub_category = models.CharField(max_length=30)

    def __str__(self):
        """
        Returns a human-readable string representation of the category.

        Returns:
            str: A string representing the category, typically the main category name.
        """
        return self.main_category



class Unit(CommonInfo):
    unit_name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=5)

    def __str__(self):
        return self.short_name


class Product(CommonInfo):
    product_name = models.CharField(max_length=100)
    product_type = models.CharField(choices=PRODUCT_TYPE_CHOICES, max_length=30)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="product_category"
    )
    product_code = models.CharField(max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="brand")
    barcode = models.CharField(max_length=100)
    product_unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name="product_unit"
    )
    product_price = models.FloatField()
    expense = models.FloatField()
    unit_price = models.FloatField()
    product_tax = models.CharField(choices=PRODUCT_TAX, max_length=10)
    tax_method = models.CharField(choices=TAX_METHOD, max_length=20)
    discount = models.FloatField()
    stock_alert = models.IntegerField()
    product_image = models.ImageField(upload_to="profile/", blank=True, null=True)
    featured = models.BooleanField(default=False)
    price_difference_in_warehouse = models.BooleanField(default=True)
    warehouse = models.ManyToManyField(Warehouse)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="product_user"
    )
    has_expiry_date = models.BooleanField(default=True)
    add_promotional_sale = models.BooleanField(default=True)
    has_multi_variant = models.BooleanField(default=True)
    has_imie_code = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        current_user = get_request().user
        self.user = current_user
        self.created_by = current_user
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name


class Barcode(CommonInfo):
    information = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="barcode_info"
    )
    barcode_image = models.ImageField(upload_to="barcode-image/", blank=True, null=True)
    papersize = models.CharField(choices=BARCODE_PAPER_SIZE, max_length=20)


class Adjustment(CommonInfo):
    warehouse = models.OneToOneField(
        Warehouse, on_delete=models.SET_NULL, null=True, blank=True
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    type = models.CharField(choices=ADJUSTMENT_TYPE,max_length=15,default=ADJUSTMENT_TYPE[0][0])

    def __str__(self) -> str:
        return self.warehouse


class Purchase(CommonInfo):
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_warehouse",
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_supplier",
    )
    product = models.ManyToManyField(Product)
    quantity = models.IntegerField(null=True,blank=True)
    order_tax = models.CharField(choices=ORDER_TAX, max_length=10)
    order_discount = models.FloatField()
    shipping = models.FloatField()
    sales_status = models.CharField(choices=SALE_STATUS, max_length=15)
    purchase_note = models.TextField()

    # def __str__(self) -> str:
    #     return self.product.product_name


class Sales(CommonInfo): 
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_customer",
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_warehouse",
    )
    biller = models.ForeignKey(
        Biller, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_biller"
    )
    product = models.ManyToManyField(Product)
    sales_tax = models.CharField(choices=ORDER_TAX, max_length=10)
    discount = models.FloatField()
    shipping = models.FloatField()
    quantity = models.IntegerField(null=True,blank=True)
    sales_status = models.CharField(choices=SALE_STATUS, max_length=15)
    payment_status = models.CharField(choices=SALE_STATUS, max_length=15)
    sales_image = models.ImageField(upload_to="sales/", blank=True, null=True)
    sales_note = models.TextField()
    staff_remark = models.TextField()

    

class Invoice(CommonInfo):
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_warehouse",
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_supplier",
    )

    class Meta:
        abstract = True


class PurchaseInvoice(Invoice):
    purchases = models.OneToOneField(
        Purchase, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.purchases.product


class SalesInvoice(Invoice):
    sales = models.OneToOneField(
        Sales, on_delete=models.SET_NULL, null=True, blank=True
    )
