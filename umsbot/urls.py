from django.conf.urls import url
from umsbot import views


urlpatterns = [
               url(r'^webhook/$', views.webhook, name='webhook'),
               url(r'^309803225:AAEfkOtjUfLCTSHicJD05uy7AvilTCkzOYs/$', views.getUpdate, name='get_update'),

               ]
