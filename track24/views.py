#!/usr/bin/python3
# -*- coding: utf-8 -*-
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
import datetime
import json
import requests
from django.utils import timezone
from django.core.urlresolvers import reverse


def main(request):

     return render(request, "index.html")

def ChooseCustomer(request):
    try:
         if(request.session["customer_token"]):
              return CustomerOrders(request)
         else:
             return render(request, "client-auth.html")
    except:
        return render(request, "client-auth.html")


def ChooseDriver(request):
    try:
         if(request.session["driver_token"]):
              return DriverOrders(request)
         else:
             return render(request, "carrier-auth.html")
    except:
        return render(request, "carrier-auth.html")



def logInCustomer(request):
    phone_number = request.POST["phone_number"]

    postData = {'phoneNumber': phone_number,"userType":"1"}
    url = 'http://track24.beetechno.uz/api/'
    if(len(phone_number) != 13 ):
         return render(request, "NumberError.html")

    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    token = dataBody["token"]
    request.session["customer_token"] = token

    return render(request, "client-auth-sms.html")


def ClientSmsVerification(request):
    token = None
    try:
        sms_code = request.POST["sms_code"]
        token = request.session["customer_token"]
    except:
        return render(request, "client-auth.html")


    postData = {'smsResponse': sms_code,"token":token}
    url = 'http://track24.beetechno.uz/api/'
    if(len(sms_code) != 5 ):
         return render(request, "SmsError.html")

    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    token = dataBody["token"]
    registered = dataBody["registered"]
    request.session["customer_token"] = token
    success = dataBody["success"]

    if(not success):
        return render(request, "SmsError.html")

    if(registered):
        return CustomerOrders(request)

    else:
        return render(request, "client-sign-up.html")

def signInCustomer(request):

    url = "http://track24.beetechno.uz/api/"
    name = request.POST["userName"]
    token = request.session["customer_token"]
    postData = {"token":token,"name":name}
    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    request.session["customer_token"] = dataBody["token"]
    registered = dataBody["registered"]
    if(registered):
        return CustomerOrders(request)
    else:
        return render(request, "client-sign-up.html")



def CustomerOrders(request):
    url = "http://track24.beetechno.uz/api/customer/getOrders/"
    try:
        token = request.session["customer_token"]
    except:
        return render(request, "client-auth.html")

    postData = {"token":token}

    response = requests.post(url, data=postData)
    dataBody = json.loads(response.text)
    return render(request, "client.html",dataBody)


def OrderDetailsForCustomer(request):
    order_id = request.POST["order_id"]
    token = "86b9eba37d8284a4"+order_id+"ad0447ce737d8885"
    postData = {'token': token}
    url = 'http://track24.beetechno.uz/api/customer/getOrderInfo/'
    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]

    return render(request, "client-more.html",dataBody)

def AcceptedOrderDetailsForCustomer(request):
    order_id = request.POST["order_id"]
    token = "86b9eba37d8284a4"+order_id+"ad0447ce737d8885"
    postData = {'token': token}
    url = 'http://track24.beetechno.uz/api/customer/acceptedOrderInfo/'
    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]

    return render(request, "client-accepted-order-info.html",{"order":dataBody})


def GoToAddOrder(request):
    return render(request, "client-add.html")

def AddOrder(request):

    url = "http://track24.beetechno.uz/api/customer/addOrders/"
    token = request.session["customer_token"]
    carTypeId = 1
    lat_from = 41.357791
    long_from = 69.246017
    lat_to = 41.363698
    long_to = 69.253581
    notes = request.POST["notes"]
    date = "16.05.2017"
    postData = {"token":token,"carTypeId":str(carTypeId),"lat_from":str(lat_from),"long_from":str(long_from),"lat_to":str(lat_to),"long_to":str(long_to),"notes":notes,"date":date}

    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    return CustomerOrders(request)


def FinishOrderCustomer(request):

    order_id = request.POST["order_id"]
    customer_token = request.session["customer_token"]
    order_token = "86b9eba37d8284a4"+order_id+"ad0447ce737d8885"
    postData = {'token': order_token,"userToken":customer_token}
    url = 'http://track24.beetechno.uz/api/customer/closeOrder/'

    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    return CustomerOrders(request)


def logInDriver(request):
    phone_number = request.POST["phone_number"]

    postData = {'phoneNumber': phone_number,"userType":"2"}
    url = 'http://track24.beetechno.uz/api/'
    if (len(phone_number) != 13):
        return render(request, "NumberError.html")

    dataBody = MakeRequest(urlPath=url, post_data=postData)[0]
    token = dataBody["token"]
    request.session["driver_token"] = token

    return render(request, "carrier-auth-sms.html")


def DriverSmsVerification(request):
    token = None
    try:
        sms_code = request.POST["sms_code"]
        token = request.session["driver_token"]
    except:
        return render(request, "carrier-auth.html")


    postData = {'smsResponse': sms_code,"token":token}
    url = 'http://track24.beetechno.uz/api/'
    if(len(sms_code) != 5 ):
         return render(request, "SmsError.html")

    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    token = dataBody["token"]
    registered = dataBody["registered"]
    request.session["driver_token"] = token
    success = dataBody["success"]

    if(not success):
        return render(request, "SmsError.html")

    if(registered):
        return DriverOrders(request)

    else:
        return render(request, "carrier-sign-up.html")

def signInDriver(request):

    url = "http://track24.beetechno.uz/api/"
    name = request.POST["userName"]
    token = request.session["driver_token"]
    maxWeight = request.POST["maxWeight"]
    carNumber = request.POST["carNumber"]
    detail = request.POST["detail"]
    carTypeId = 2

    postData = {"token":token,"name":name,"maxWeight":maxWeight,"carNumber":carNumber,"detail":detail,"carTypeId":carTypeId}
    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    request.session["driver_token"] = dataBody["token"]
    registered = dataBody["registered"]
    if(registered):
        return DriverOrders(request)
    else:
        return render(request, "carrier-sign-up.html")

def DriverOrders(request):
    get_orders_url = "http://track24.beetechno.uz/api/driver/getOrders/"
    url_for_accepted_orders = "http://track24.beetechno.uz/api/driver/myOrders/"

    try:
        token = request.session["driver_token"]
    except:
        return render(request, "carrier-auth.html")

    postData = {"token":token}
    orders =  MakeRequest(urlPath=get_orders_url, post_data=postData)
    accepted_orders = MakeRequest(urlPath=url_for_accepted_orders, post_data=postData)
    print(token)
    return render(request, "carrier.html",{"accepted_orders":accepted_orders,"orders":orders})


def OrderDetailsForDriver(request):
    order_id = request.POST["order_id"]
    driver_token = request.session["driver_token"]

    order_token = "86b9eba37d8284a4"+order_id+"ad0447ce737d8885"
    postData = {'token': order_token,"userToken":driver_token}
    url = 'http://track24.beetechno.uz/api/driver/getOrderInfo/'
    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    print(dataBody)
    return render(request, "driver-order-info.html",{"order":dataBody})


def FinishOrderDriver(request):

    order_id = request.POST["order_id"]
    driver_token = request.session["driver_token"]
    order_token = "86b9eba37d8284a4"+order_id+"ad0447ce737d8885"
    postData = {'token': order_token,"userToken":driver_token}
    url = 'http://track24.beetechno.uz/api/driver/closeOrder/'

    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    return DriverOrders(request)


def OffersList(request):

    order_id = request.POST["order_id"]
    order_token = "86b9eba37d8284a4"+order_id+"ad0447ce737d8885"
    postData = {'token': order_token}
    url = 'http://track24.beetechno.uz/api/customer/getOffers/'
    dataBody = MakeRequest(urlPath=url,post_data=postData)
    return  render(request, "client-more-offers.html",{"offers":dataBody})

def OfferInfo(request):

    offer_id = request.POST["offer_id"]
    offer_token = "86b9eba37d8284a4"+offer_id+"ad0447ce737d8885"
    postData = {'token': offer_token}
    url = 'http://track24.beetechno.uz/api/customer/getOfferInfo/'
    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    return render(request, "client-more-offers-about.html",{"offer":dataBody})

def OfferPrice(request):

    try:
        userId = request.session["driver_token"]
    except:
        return render(request, "carrier-auth.html")

    price = request.POST["price"]
    orderId = request.POST["orderId"]
    order_token = "86b9eba37d8284a4"+orderId+"ad0447ce737d8885"
    postData = {'token': order_token,"userId":userId,"price":price}
    url = 'http://track24.beetechno.uz/api/driver/makeOffer/'
    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    return DriverOrders(request)

def AcceptOffer(request):

    offer_id = request.POST["offer_id"]
    offer_token = "86b9eba37d8284a4"+offer_id+"ad0447ce737d8885"
    postData = {'token': offer_token}
    url = 'http://track24.beetechno.uz/api/customer/acceptOffer/'
    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    return CustomerOrders(request)


def MakeRequest(urlPath,post_data):
    response = requests.post(urlPath, data=post_data)
    dataBody = json.loads(response.text)['data']
    return dataBody


