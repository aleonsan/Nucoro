"""NucoroCurrencyDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views



from .views import *

urlpatterns = [
    path('', index),
    path('mockdata/<int:year>-<int:month>-<int:day>', mockdata),
    path('timeseries/', timeseries.as_view()),
    path('timeseries2/', timeseries2.as_view()),
    path('calculator/', calculator.as_view()),
    path('time_weighted_rate/', time_weighted_rate.as_view()),
    path('backoffice/', login_required(backoffice.as_view())),
    path('accounts/login/', auth_views.LoginView.as_view()),
]
