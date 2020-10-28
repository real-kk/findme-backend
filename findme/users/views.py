
from django.shortcuts import render
from .models import User
from django.http import HttpResponse,JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi
import json
from django.core.serializers import serialize
test_param = openapi.Parameter('test', openapi.IN_QUERY, type=openapi.TYPE_STRING)

@swagger_auto_schema(method='get', manual_parameters=[test_param])
@api_view(['GET'])
def EamilRedundantCheck(request):
    """
    이메일 중복 체크 API

    ---
    # /users/email/
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



@swagger_auto_schema(method='get', manual_parameters=[test_param])
@api_view(['GET'])
def getUserListsByUserType(request):
    """
    내담자/상담자 리스트 조회 API

    ---
    # /users/
    ## query parameter
        - user_type : 상담자/내담자 구분 ( 내담자 : 0 ,상담자 : 1 )
    """
    if request.method == "GET":
        user_type = request.GET.get("user_type")
        try:
            list = User.objects.filter(user_type=user_type)
            userExist = len(list)
        except:
            return HttpResponse('Server Error',status=404)
        data = json.loads(serialize('json', list,fields=('email','user_type','username')))
        if userExist == False:
            return HttpResponse('Users Not Exists',status=403)
        else:
            return JsonResponse({'message':'Users Exists','users': data},status=200)
