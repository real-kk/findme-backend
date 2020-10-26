
from django.shortcuts import render
from .models import User
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi

test_param = openapi.Parameter('test', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)

@swagger_auto_schema(method='get', manual_parameters=[test_param])
@api_view(['GET'])
def EamilRedundantCheck(request):
    """
    이메일 중복 체크 API

    ---
    # /email/
    ## query parameter
        - email : 중복 체크하려는 이메일
    """
    if request.method == "GET":
        email = request.GET.get("email")
        try:
            userExist=len(User.objects.filter(email=email))
        except:
            return HttpResponse('Server Error',status=404)

        
        if userExist ==False:
            return HttpResponse('Email Available',status=200)
        else:
            return HttpResponse('Email Redundant',status=403)
