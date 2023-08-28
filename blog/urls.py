"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from blog import views
from .views import ShowProfile

urlpatterns = [
    path("", views.index, name="bloghome"),
    path("about/", views.about, name="blogabout"),
    path("contact/", views.contact, name="blogcontact"),
    path("blogger/", views.blogger, name="blogblogger"),
    path("postcomment/", views.postcomment, name="bloggsign"),
    path("search/", views.search, name="blogblogger"), 
    path("signup/", views.handlesignup, name="bloggsign"),
    path("userlogin/", views.userlogin, name="bloggsign"),
    path("userlogout/", views.userlogout, name="bloggsign"),
    path("make/", views.make, name="blogpost"),
    path('profile/', views.profile, name='profile'),
    path("<int:pk>/profile", ShowProfile.as_view(), name="ShowProfile"),

    path("<str:slug>/", views.blogpost, name="blogpost"),

]
