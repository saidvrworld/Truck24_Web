from django.conf.urls import url
from umsbot import views


urlpatterns = [
               url(r'^webhook/$', views.webhook, name='webhook'),
               url(r'^359231813:AAGTeb93BP9Gg-SDGPzpUAcvQdAzjd_qUe0/$', views.getUpdate, name='get_update'),

               ]
