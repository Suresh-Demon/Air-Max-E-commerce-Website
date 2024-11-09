from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class productdata(models.Model):
    pcat=((1,'Shoes'),(2,'T-Shirts'),(3,'Shorts'))
    name=models.CharField(max_length=100)
    pdetails=models.CharField(max_length=100,verbose_name="Product Details")
    pcat=models.IntegerField(verbose_name="Category",choices=pcat)
    price=models.FloatField()
    is_active=models.BooleanField(default=True,verbose_name="Available")
    pimage=models.ImageField(upload_to='images')

def __str__(self):
    return self.name

class cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(productdata,on_delete=models.CASCADE,db_column="pid")  
    qty=models.IntegerField(default=1)   


class order(models.Model):
    order_id=models.CharField(max_length=100)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(productdata,on_delete=models.CASCADE,db_column="pid")  
    qty=models.IntegerField(default=1)      