from django.contrib import admin
from .models import productdata

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_filter=['pcat','is_active']
    
admin.site.register(productdata,ProductAdmin)