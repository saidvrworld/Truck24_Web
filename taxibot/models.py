# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models




class TaxiCall(models.Model):

    call_id = models.AutoField(primary_key=True)
    chat_id = models.IntegerField(default=0)
    IsMap = models.BooleanField()
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    address = models.CharField(max_length=500,default="None")
    type = models.CharField(max_length=100,default="None")
    number = models.CharField(max_length=20,default="None")
    details = models.CharField(max_length=500,default="None")
    call_time = models.TimeField(auto_now=True)
    status = models.CharField(max_length=30,default="new")
    waiting_for = models.CharField(max_length=40,default="None")

class Car(models.Model):

    car_type = models.CharField(max_length=200)
    car_number = models.CharField(max_length=20)
    car_time = models.IntegerField(default=0)
    driver_number = models.CharField(max_length=30,default="недоступен")
    taxi = models.ForeignKey(TaxiCall)

