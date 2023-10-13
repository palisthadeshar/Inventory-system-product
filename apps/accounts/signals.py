from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import Biller
from decouple import config

@receiver(post_save, sender=Biller)
def biller_code(sender, instance, created, **kwargs):
    BILLER_PREFIX = config("BILLER_PREFIX")
    total_biller_objects = Biller.objects.count()
    print(total_biller_objects)
    biller_code=f"{BILLER_PREFIX}{total_biller_objects}"
    
    if created:
        instance.biller_code = biller_code
        instance.save()
