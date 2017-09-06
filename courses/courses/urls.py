from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^courses/', include('courses_site.urls')),
    url(r'^admin/', admin.site.urls),
]