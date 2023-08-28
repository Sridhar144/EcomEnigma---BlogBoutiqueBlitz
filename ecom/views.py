from django.shortcuts import render,HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    
    return render(request, 'index.html')