from django.contrib import admin
from django.urls import path, include

import safadordelasdelicias

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('safadordelasdelicias.urls')),
    path('safadordelasdelicias/' , include('safadordelasdelicias.urls')),
]
