
from django.db.models.signals import post_save, pre_delete, pre_save

from django.dispatch import receiver
from .models import Bank, CustomerAccount


@receiver(post_save, sender=CustomerAccount)
def create_bank_details(sender, instance, created, **kwargs):
    
    if created:
        Bank.objects.create(customer=instance)
       

@receiver(post_save, sender=CustomerAccount)
def save_profile(sender, instance, **kwargs):
		instance.bank.save()
