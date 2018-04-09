# -*- coding:utf-8 -*-
from django.db import models


class UserInfo(models.Model):
    uname = models.CharField(max_length=20,unique=True)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    # default,blank是python层面的约束不用重新迁移


class AddrInfo(models.Model):
    ushou = models.CharField(max_length=20)
    uaddress = models.CharField(max_length=100)
    uyoubian = models.CharField(max_length=6)
    user = models.ForeignKey('UserInfo')
    uphone = models.CharField(max_length=11, default='')
