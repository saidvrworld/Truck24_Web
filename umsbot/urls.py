from django.conf.urls import url
from umsbot import views


urlpatterns = [
               url(r'^webhook/$', views.webhook, name='webhook'),
               url(r'^'+views.token+'/$', views.getUpdate, name='get_update'),

               ]
