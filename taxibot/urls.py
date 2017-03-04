from django.conf.urls import url
from taxibot import views


urlpatterns = [url(r'^$', views.CallListView.as_view(), name='callList'),
               url(r'^setDriver/$',views.setDriver, name='setDriver'),
               url(r'^clearDB/$', views.clearDB, name='clearDB'),
               url(r'^callsWithCar/$', views.calls_with_car_ListView.as_view(), name='calls_with_car'),
               url(r'^accepted/$', views.acceptedCalls.as_view(), name='accepted'),
               url(r'^createBot/$', views.CreateBot, name='create_bot'),
               url(r'^setArrived/$', views.EndCall, name='send_arrived'),
               url(r'^webhook/$', views.webhook, name='webhook'),
               url(r'^getupdate/$', views.getUpdate, name='get_update'),

               ]
