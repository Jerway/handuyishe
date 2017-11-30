from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_num = models.CharField(max_length=20, blank=True)

    class Meta(AbstractUser.Meta):
        pass


class ProType(models.Model):
    tid = models.IntegerField()
    total = models.IntegerField()
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'protype'


class Product(models.Model):
    pid = models.IntegerField()
    name = models.CharField(max_length=200)
    imgurl = models.CharField(max_length=300)
    price = models.CharField(max_length=10)
    ptype = models.ForeignKey(ProType)

    class Meta:
        db_table = 'product'
