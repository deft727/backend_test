from django.contrib import admin

from payments.models import Customer, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class ChargeAdmin(admin.ModelAdmin):
    pass
