"""myscrumy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include,path
from remiljscrumy import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('remiljscrumy/', include('remiljscrumy.urls',namespace='remiljscrumy')),
    path('add_goal/', views.add_goal,name='add_goal'),
    path('filter/',views.filterArg,name='filterArg'),
    path('index/',views.index,name='index'),
    path('home/', views.home, name='home'),
    #path('home/', views.add_goal, name='add_goal'),
    #path('index/', include('remiljscrumy.urls',namespace ='remiljscrumy')),
]
