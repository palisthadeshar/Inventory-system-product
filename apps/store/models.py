from django.db import models
from utils.models import CommonInfo, Address
from utils.validations import validate_mobile_number


# Create your models here.
class Warehouse(CommonInfo, Address):
    name = models.CharField(max_length=100)
    phone = models.CharField(
         unique=True, validators=[validate_mobile_number]
    )
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name 
