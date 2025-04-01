from django.urls import path

from safadordelasdelicias.views import *

urlpatterns = [
    path('home/', home , name='home_page'),
]