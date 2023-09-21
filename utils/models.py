from django.db import models
import uuid


class CommonInfo(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_created_by",
        null=True,
        blank=True
    )
    modified_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_modified_by",
        null=True,
        blank=True,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Address(models.Model):
    zip_code = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=False, default="Lalitpur")
    country = models.CharField(max_length=50, default="Nepal")
    street = models.CharField(max_length=50,blank=True, null=True)
    
    class Meta:
        abstract=True

