from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Register your models here.


class Imagelist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=550)


class UserImagelist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=550)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=250, null=True, default=None)


admin.site.register(Imagelist)
admin.site.register(UserImagelist)
