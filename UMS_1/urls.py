from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()


# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [url(r'^track24/', include('track24.urls', namespace='track24')),
    url(r'^admin/', admin.site.urls),
               ]

