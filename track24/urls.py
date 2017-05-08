from django.conf.urls import url
from track24 import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^main/$',views.main,name='main'),
    url(r'^client-auth/$', views.ChooseCustomer, name='chooseCustomer'),
    url(r'^driver-auth/$', views.ChooseDriver, name='chooseDriver'),

    url(r'^client-logIn/$', views.logInCustomer, name='logInCustomer'),
    url(r'^client-logOut/$', views.logOutCustomer, name='logOutCustomer'),

    url(r'^driver-logIn/$', views.logInDriver, name='logInDriver'),
    url(r'^driver-logOut/$', views.logOutDriver, name='logOutDriver'),

    url(r'^client-sms/$', views.ClientSmsVerification, name='clientSmsVerification'),
    url(r'^driver-sms/$', views.DriverSmsVerification, name='driverSmsVerification'),

    url(r'^client-signIn/$', views.signInCustomer, name='signInCustomer'),
    url(r'^driver-signIn/$', views.signInDriver, name='signInDriver'),

    url(r'^client-go-to-add-order/$', views.GoToAddOrder, name='GoToAddOrder'),
    url(r'^client-add-order/$', views.AddOrder, name='AddOrder'),
    url(r'^client-add-order-cars/$', views.ChooseTypeForAddOrder, name='ChooseCarAddOrder'),

    url(r'^client-done-orders/$', views.CustomerDoneOrders, name='DoneOrdersCustomer'),

    url(r'^client-order-details/$', views.OrderDetailsForCustomer, name='OrderDetailsForCustomer'),
    url(r'^client-accepted-order-details/$', views.AcceptedOrderDetailsForCustomer, name='AcceptedOrderDetailsForCustomer'),

    url(r'^driver-order-details/$', views.OrderDetailsForDriver, name='OrderDetailsForDriver'),

    url(r'^driver-finish-order/$', views.FinishOrderDriver, name='FinishOrderDriver'),
    url(r'^client-finish-order/$', views.FinishOrderCustomer, name='FinishOrderCustomer'),

    url(r'^client-offers-list/$', views.OffersList, name='OffersList'),
    url(r'^client-offer-info/$', views.OfferInfo, name='OfferInfo'),
    url(r'^client-offer-accept/$', views.AcceptOffer, name='AcceptOffer'),
    url(r'^driver-offer-price/$', views.OfferPrice, name='OfferPrice'),

    url(r'^driver-profile/$', views.driverSettings, name='driverSettings'),
    url(r'^driver-profile/loadUserPhoto$', views.LoadUserPhoto, name='loadUserPhoto'),
    url(r'^driver-profile/loadCarPhoto$', views.LoadCarPhoto, name='loadCarPhoto'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
