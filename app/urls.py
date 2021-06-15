"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path
from users_manager import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home_unloged'),
    path('home', views.index_loged, name='home'),
    path('login/', LoginView.as_view(), {'template_name':'login.html'}, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('sign-up/', views.UserSignUp.as_view(), name='sign-up'),
    path('profile-form/', views.profile_form, name='profile-form'),
    path('modelo/',views.modelo, name="modelo"), #se enlaza con la vista modelo
    path('clasificador/',views.clasificador, name= "clasificador"),
    path('upload/', views.entrada, name = "subida"),
    path('listaArchivos/', views.file_list, name = "listaArchivos"),
    
    path('ingreso', views.ingreso_chat, name = "ingreso_chat"),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('guardar/<str:room>',views.guardarConv, name = 'guardarConv'),
    
    url(r'^accounts/login/$', views.profile_form),
    url(r'^classifier/(?P<id_file>\d+)/$', views.file_classifier, name= "clasificador"),
    url(r'^delete/(?P<id_file>\d+)/$', views.file_delete, name= "delete-file"),
]
