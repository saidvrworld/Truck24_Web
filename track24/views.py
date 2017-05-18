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
from django.core.files.storage import FileSystemStorage
from requests_toolbelt.multipart.encoder import MultipartEncoder
from django.conf import settings
import os
from PIL import Image


def main(request):

    lang = getLanguage(request)
    return render(request,lang + "/index.html")


########################################################################################################################
#   CUSTOMER  CLASSES
########################################################################################################################

def ChooseCustomer(request):

    lang = getLanguage(request)

    try:
         if(request.session["customer_token"]):
              return CustomerOrders(request)
         else:

             return render(request, lang + "client-auth.html")
    except:
        return render(request, lang + "client-auth.html")


def ChooseDriver(request):
    lang = getLanguage(request)

    try:
         if(request.session["driver_token"]):
              return DriverOrders(request)
         else:
             return render(request, lang + "carrier-auth.html")
    except:
        return render(request, lang + "carrier-auth.html")



def logInCustomer(request):

    lang = getLanguage(request)
    phone_number = request.POST["phone_number"]

    postData = {'phoneNumber': phone_number,"userType":"1"}
    url = 'http://track24.beetechno.uz/api/'
    if(len(phone_number) != 13 ):
         return render(request, lang + "NumberError.html")

    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    token = dataBody["token"]
    request.session["customer_token"] = token

    return render(request, lang + "client-auth-sms.html")

def logOutCustomer(request):

    lang = getLanguage(request)
    request.session["customer_token"] = None
    return render(request, lang + "client-auth.html")


def ClientSmsVerification(request):
    lang = getLanguage(request)
    token = None
    try:
        sms_code = request.POST["sms_code"]
        token = request.session["customer_token"]
    except:
        return render(request, lang + "client-auth.html")


    postData = {'smsResponse': sms_code,"token":token}
    url = 'http://track24.beetechno.uz/api/'
    if(len(sms_code) != 5 ):
         return render(request, lang + "SmsError.html")

    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    token = dataBody["token"]
    registered = dataBody["registered"]
    request.session["customer_token"] = token
    success = dataBody["success"]

    if(not success):
        return render(request, lang + "SmsError.html")

    if(registered):
        return CustomerOrders(request)

    else:
        return render(request, lang + "client-sign-up.html")

def signInCustomer(request):
    lang = getLanguage(request)

    try:
        token = request.session["customer_token"]
    except:
        return render(request, lang + "client-auth.html")


    url = "http://track24.beetechno.uz/api/"
    name = request.POST["userName"]
    if(len(name)==0):
        return render(request, lang + "NameError.html")

    postData = {"token":token,"name":name}
    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    request.session["customer_token"] = dataBody["token"]
    registered = dataBody["registered"]
    if(registered):
        return CustomerOrders(request)
    else:
        return render(request, lang + "client-sign-up.html")


def CustomerOrders(request):

    lang = getLanguage(request)
    url = "http://track24.beetechno.uz/api/customer/getOrders/"
    try:
        token = request.session["customer_token"]
    except:
        return render(request, lang + "client-auth.html")

    postData = {"token":token}

    response = requests.post(url, data=postData)
    dataBody = json.loads(response.text)
    return render(request, lang + "client.html",dataBody)

def CustomerDoneOrders(request):

    lang = getLanguage(request)
    url = "http://track24.beetechno.uz/api/customer/getFinishedOrders/"
    try:
        token = request.session["customer_token"]
    except:
        return render(request, lang + "client-auth.html")

    postData = {"token":token}

    response = requests.post(url, data=postData)
    dataBody = json.loads(response.text)
    return render(request, lang + "client-done-orders.html",dataBody)


def OrderDetailsForCustomer(request):
    lang = getLanguage(request)

    order_id = request.POST["order_id"]
    token = "86b9eba37d8284a4"+order_id+"ad0447ce737d8885"
    postData = {'token': token}
    url = 'http://track24.beetechno.uz/api/customer/getOrderInfo/'
    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    from_address = getAddress(dataBody["from_lat"],dataBody["from_long"])
    to_address = getAddress(dataBody["to_lat"],dataBody["to_long"])
    print(dataBody)
    return render(request, lang + "client-more.html",{"order":dataBody,"from_address":from_address,"to_address":to_address})

def AcceptedOrderDetailsForCustomer(request):
    lang = getLanguage(request)

    order_id = request.POST["order_id"]
    token = "86b9eba37d8284a4"+order_id+"ad0447ce737d8885"
    postData = {'token': token}
    url = 'http://track24.beetechno.uz/api/customer/acceptedOrderInfo/'
    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    from_address = getAddress(dataBody["lat_from"], dataBody["long_from"])
    to_address = getAddress(dataBody["lat_to"], dataBody["long_to"])

    try:
        driverLat = dataBody["userLat"]
        driverLong = dataBody["userLong"]
    except:
        driverLat = 0
        driverLong = 0


    return render(request, lang + "client-accepted-order-info.html",{"order":dataBody,"from_address":from_address,"to_address":to_address,"driverLat":driverLat,"driverLong":driverLong})


def GoToAddOrder(request):
    return CarTypesCustomer(request)

def AddOrder(request):
    lang = getLanguage(request)

    url = "http://track24.beetechno.uz/api/customer/addOrders/"
    try:
        token = request.session["customer_token"]
    except:
        return render(request, lang + "client-auth.html")

    try:
        carTypeId = request.session["carId"]
    except:
        return AddOrder(request)

    try:

        lat_from = request.POST["from_lat"]
        long_from = request.POST["from_long"]
        lat_to = request.POST["to_lat"]
        long_to = request.POST["to_long"]
        notes = request.POST["notes"]
        day = request.POST["day"]
        month = request.POST["month"]
        year = request.POST["year"]
        date = day+"."+month+"."+year
    except:
        return render(request, lang + "FieldsEmptyError.html")

    if(len(notes) == 0):
        notes = "Нужно быстро доставить товар"
    postData = {"token":token,"carTypeId":str(carTypeId),"lat_from":str(lat_from),"long_from":str(long_from),"lat_to":str(lat_to),"long_to":str(long_to),"notes":notes,"date":date}
    print(postData)
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


def OffersList(request):
    lang = getLanguage(request)

    order_id = request.POST["order_id"]
    order_token = "86b9eba37d8284a4"+str(order_id)+"ad0447ce737d8885"
    postData = {'token': order_token}
    url = 'http://track24.beetechno.uz/api/customer/getOffers/'
    dataBody = MakeRequest(urlPath=url,post_data=postData)
    return  render(request, lang + "client-more-offers.html",{"offers":dataBody})

def OfferInfo(request):
    lang = getLanguage(request)

    offer_id = request.POST["offer_id"]
    offer_token = "86b9eba37d8284a4"+offer_id+"ad0447ce737d8885"
    postData = {'token': offer_token}
    url = 'http://track24.beetechno.uz/api/customer/getOfferInfo/'
    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    return render(request, lang + "client-more-offers-about.html",{"offer":dataBody})


def AcceptOffer(request):

    offer_id = request.POST["offer_id"]
    offer_token = "86b9eba37d8284a4"+offer_id+"ad0447ce737d8885"
    postData = {'token': offer_token}
    url = 'http://track24.beetechno.uz/api/customer/acceptOffer/'
    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    return CustomerOrders(request)

def CarTypesCustomer(request):
    lang = getLanguage(request)

    get_carType_url = "http://track24.beetechno.uz/api/customer/carTypes/"

    try:
        token = request.session["customer_token"]
    except:
        return render(request, lang + "client-auth.html")

    postData = {"token":token}
    types =  MakeRequest(urlPath=get_carType_url, post_data=postData)
    return render(request, lang + "chooseType.html",{"types":types})

def ChooseTypeForAddOrder(request):
    lang = getLanguage(request)

    type_id = request.POST["carTypeId"]
    request.session["carId"] = type_id

    return render(request, lang + "client-add.html")


########################################################################################################################
#   DRIVER  CLASSES
########################################################################################################################

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

def logOutDriver(request):

    request.session["driver_token"] = None
    return render(request, "carrier-auth.html")


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
        return CarTypesDriver(request)


def CarTypesDriver(request):
    get_carType_url = "http://track24.beetechno.uz/api/customer/carTypes/"

    try:
        token = request.session["driver_token"]
    except:
        return render(request, "carrier-auth.html")

    postData = {"token":token}
    types =  MakeRequest(urlPath=get_carType_url, post_data=postData)
    return render(request, "chooseTypeDriver.html",{"types":types})

def ChooseTypeForDriver(request):
    type_id = request.POST["carTypeId"]
    request.session["carId"] = type_id

    return render(request, "carrier-sign-up.html")


def signInDriver(request):
    try:
        carTypeId = request.session["carId"]
    except:
        return CarTypesDriver(request)

    url = "http://track24.beetechno.uz/api/"
    name = request.POST["userName"]
    token = request.session["driver_token"]
    maxWeight = request.POST["maxWeight"]
    carNumber = request.POST["carNumber"]
    detail = request.POST["detail"]

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
    for order in  orders:
        from_address = getAddress(order["from_lat"], order["from_long"])
        order["from_address"] = from_address
    accepted_orders = MakeRequest(urlPath=url_for_accepted_orders, post_data=postData)
    print(token)
    return render(request, "carrier.html",{"accepted_orders":accepted_orders,"orders":orders})

def DriverFinishedOrders(request):
    url_for_finished_orders = "http://track24.beetechno.uz/api/driver/myFinishedOrders/"

    try:
        token = request.session["driver_token"]
    except:
        return render(request, "carrier-auth.html")

    postData = {"token":token}
    orders =  MakeRequest(urlPath=url_for_finished_orders, post_data=postData)

    print(token)
    return render(request, "carrier-finished-orders.html",{"finished_orders":orders})


def OrderDetailsForDriver(request):
    order_id = request.POST["order_id"]
    driver_token = request.session["driver_token"]

    order_token = "86b9eba37d8284a4"+order_id+"ad0447ce737d8885"
    postData = {'token': order_token,"userToken":driver_token}
    url = 'http://track24.beetechno.uz/api/driver/getOrderInfo/'
    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    from_address = getAddress(dataBody["from_lat"], dataBody["from_long"])
    to_address = getAddress(dataBody["to_lat"], dataBody["to_long"])

    print(dataBody)
    return render(request, "driver-order-info.html",{"order":dataBody,"from_address":from_address,"to_address":to_address})


def FinishOrderDriver(request):

    order_id = request.POST["order_id"]
    driver_token = request.session["driver_token"]
    order_token = "86b9eba37d8284a4"+order_id+"ad0447ce737d8885"
    postData = {'token': order_token,"userToken":driver_token}
    url = 'http://track24.beetechno.uz/api/driver/closeOrder/'

    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    return DriverOrders(request)



def OfferPrice(request):

    try:
        userId = request.session["driver_token"]
    except:
        return render(request, "carrier-auth.html")

    price = request.POST["price"]
    if(len(price) == 0):
        return render(request, "PriceError.html")

    orderId = request.POST["orderId"]
    order_token = "86b9eba37d8284a4"+orderId+"ad0447ce737d8885"
    postData = {'token': order_token,"userId":userId,"price":price}
    url = 'http://track24.beetechno.uz/api/driver/makeOffer/'
    dataBody = MakeRequest(urlPath=url,post_data=postData)[0]
    return DriverOrders(request)


def driverSettings(request):
    try:
        userId = request.session["driver_token"]
    except:
        return render(request, "carrier-auth.html")

    postData = {'token': userId}
    url = 'http://track24.beetechno.uz/api/driver/getDriverInfo/'

    dataBody = MakeRequest(urlPath=url, post_data=postData)[0]

    return render(request, "carrier-profile.html",{"driver":dataBody})




def LoadUserPhoto(request):

    try:
        userId = request.session["driver_token"]
    except:
        return render(request, "carrier-auth.html")

    if request.method == 'POST' and request.FILES['userPhoto']:
        myfile = request.FILES['userPhoto']
        fs = FileSystemStorage()
        filename = fs.save(userId+".jpg", myfile)
        Compress(os.path.join(settings.MEDIA_ROOT, userId+".jpg"))
        return SendMultipartUser(request,userId)

    return driverSettings(request)

def SendMultipartUser(request,fileName):

    multipart_data = MultipartEncoder(
        fields={
            'userPhoto': ( fileName + ".jpg",open(os.path.join(settings.MEDIA_ROOT, fileName + ".jpg"), 'rb'),),
        }
    )
    response = requests.post('http://track24.beetechno.uz/api/driver/uploadPhoto/', data=multipart_data,
                             headers={'Content-Type': multipart_data.content_type})
    os.remove(os.path.join(settings.MEDIA_ROOT, fileName + ".jpg"))
    return driverSettings(request)

def LoadCarPhoto(request):

    try:
        userId = request.session["driver_token"]
    except:
        return render(request, "carrier-auth.html")

    if request.method == 'POST' and request.FILES['carPhoto']:
        myfile = request.FILES['carPhoto']
        fs = FileSystemStorage()
        filename = fs.save(userId+".jpg", myfile)
        return SendMultipartCar(request,userId)

    return driverSettings(request)

def SendMultipartCar(request,fileName):

    multipart_data = MultipartEncoder(
        fields={
            'carPhoto': ( fileName + ".jpg",open(os.path.join(settings.MEDIA_ROOT, fileName + ".jpg"), 'rb'),),
        }
    )
    response = requests.post('http://track24.beetechno.uz/api/driver/uploadPhoto/', data=multipart_data,
                             headers={'Content-Type': multipart_data.content_type})
    os.remove(os.path.join(settings.MEDIA_ROOT, fileName + ".jpg"))
    return driverSettings(request)




####################################################################################################################################

def MakeRequest(urlPath,post_data):
    response = requests.post(urlPath, data=post_data)
    dataBody = json.loads(response.text)['data']
    return dataBody


def getAddress(lat,long):

    url = "http://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lat)+","+str(long)+"&sensor=true&language=russian"
    try:
        response = requests.post(url)

        dataBody = json.loads(response.text)['results']
        finalAddress = dataBody[0]["formatted_address"]
    except:
        print(dataBody)
        finalAddress = "Не удалось определить аддресс"

    return finalAddress


def Compress(filePath):

    imgobj = Image.open(filePath)
    imgobj.thumbnail((400,400), Image.ANTIALIAS)
    imgobj.save(filePath)


def getLanguage(request):
    try:
        lang = request.session["language"]
    except:
        request.session["language"] = "ru"
        lang = request.session["language"]

    return lang