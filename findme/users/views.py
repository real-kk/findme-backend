
from django.shortcuts import render
from .models import User
from django.http import HttpResponse

def EamilRedundantCheck(request) :
    if request.method == "GET":
        email = request.GET.get("email")
        try:
            userExist=len(User.objects.filter(email=email))
        except:
            return HttpResponse('Server Error',status=403)

        
        if userExist ==False:
            return HttpResponse('Email Available',status=200)
        else:
            return HttpResponse('Email Redundant',status=403)
