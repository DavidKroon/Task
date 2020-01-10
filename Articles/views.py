from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.

content=User.objects.all();

def articleshome(request):
    return HttpResponse(content)  #returns queryset