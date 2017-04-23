from django.conf.urls import url
from track24 import views


urlpatterns = [
    url(r'^main/$',views.main,name='main'),
    url(r'^client-auth/$', views.ChooseCustomer, name='chooseCustomer'),
    url(r'^driver-auth/$', views.ChooseDriver, name='chooseDriver'),

    url(r'^client-logIn/$', views.logInCustomer, name='logInCustomer'),
    url(r'^driver-logIn/$', views.logInDriver, name='logInDriver'),

    url(r'^client-signIn/$', views.signInCustomer, name='signInCustomer'),
    url(r'^driver-signIn/$', views.signInDriver, name='signInDriver'),

    url(r'^client-go-to-add-order/$', views.GoToAddOrder, name='GoToAddOrder'),
    url(r'^client-add-order/$', views.AddOrder, name='AddOrder'),

    url(r'^client-order-details/$', views.OrderDetailsForCustomer, name='OrderDetailsForCustomer'),
    url(r'^driver-order-details/$', views.OrderDetailsForDriver, name='OrderDetailsForDriver'),

    url(r'^driver-finish-order/$', views.FinishOrderDriver, name='FinishOrderDriver'),
    url(r'^client-offers-list/$', views.OffersList, name='OffersList'),
    url(r'^client-offer-info/$', views.OfferInfo, name='OfferInfo'),
    url(r'^client-offer-accept/$', views.AcceptOffer, name='AcceptOffer'),

]
