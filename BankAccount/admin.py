from django.contrib import admin
from .models import *

admin.site.register(Bank)
admin.site.register(CustomerAccount)
admin.site.register(BankTransaction)
