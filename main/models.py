from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    number = models.CharField(max_length=15, blank=True,null=True)
    points = models.IntegerField(default=0)


class Wholesaler(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    number = models.CharField(max_length=15,blank=True,null=True)
    points = models.IntegerField(default=0)
class StoreOwner(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    number = models.CharField(max_length=15, blank=True,null=True)
    points = models.IntegerField(default=0)





class ProductMarket(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_market_images/')
    point_to_redeem = models.IntegerField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    redeemed_time = models.TimeField(null=True, blank=True)
    product = models.OneToOneField('Product', on_delete=models.CASCADE)
    redeemed_at = models.DateField(null=True, blank=True)

class Product(models.Model):
    created_at = models.DateField(auto_now_add=True)
    barcode = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    qrcode = models.ImageField(upload_to='product_qrcodes/',null=True, blank=True)
    is_redeemed = models.BooleanField(default=False)
    got_the_tokens = models.BooleanField(default=False)

class Bulk(models.Model):
    created_at = models.DateField(auto_now_add=True)
    barcode = models.CharField(max_length=255)
    qrcode = models.ImageField(upload_to='bulk_qrcodes/')
    got_the_tokens = models.BooleanField(default=False)
