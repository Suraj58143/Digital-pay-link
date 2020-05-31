"""firstproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
#from django.contrib import admin
from django.urls import include, path
from . import models
from . import forms
from . import views

urlpatterns = [
   # path('admin/', admin.site.urls),
   # path('proapp/',models.data,name='data'),
    #path('forms/',forms.fdata,name='fdata'),
    path('req/',views.req,name='req'),
    path('result.html',views.ren,name='ren'),
    path('',views.view,name='view'),
    path('login',views.log,name='log')
]
