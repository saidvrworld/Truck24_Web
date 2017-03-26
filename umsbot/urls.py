from django.conf.urls import url
from umsbot import views


urlpatterns = [
               url(r'^webhook/$', views.webhook, name='webhook'),
               url(r'^350774649:AAG5JYhMCZ2rCi7gh6OWILTru37fdPQrqhg/$', views.getUpdate, name='get_update'),

               ]
