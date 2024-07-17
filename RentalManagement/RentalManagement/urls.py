
from django.contrib import admin
from django.urls import path, include
import Rent

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api',include(Rent.urls) )
]
