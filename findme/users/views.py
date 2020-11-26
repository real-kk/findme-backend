from django.shortcuts import render
from .models import User
from django.http import HttpResponse,JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi
import json
from django.core.serializers import serialize
test_param = openapi.Parameter('test', openapi.IN_QUERY, type=openapi.TYPE_STRING)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

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
        data = json.loads(serialize('json', list,fields=('email','user_type','username','introduce')))
        if userExist == False:
            return HttpResponse('Users Not Exists',status=403)
        else:
            return JsonResponse({'message':'Users Exists','users': data},status=200)

class getEachUserType(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_type = User.objects.filter(email=request.user).values('user_type')[0]
        return JsonResponse(user_type, status=200)
class updateUserIntroduce(APIView):
    
    @csrf_exempt
    def put(self,request,**kwargs):
        """
        유저 정보 업데이트

        ---
        # /users/<id:int>/
        ## headers
            - Authorization : Token "key 값" [ex> Token 822a24a314dfbc387128d82af6b952191dd71651]
        """

        if kwargs.get('id') is None:
            return Response('invalid request', status=status.HTTP_400_BAD_REQUEST)
        else:
            user_id = kwargs.get('id')
            try:
                user_obj = User.objects.get(id=user_id)
            except:
                return Response("User not Found", status=status.HTTP_400_BAD_REQUEST)
            user_obj.introduce = request.data.get("introduce")
            user_obj.image = request.data.get("image")
            user_obj.username = request.data.get("username")
            user_obj.user_type = request.data.get("user_type")
            user_obj.password = request.data.get("password")
            
            user_obj.save()
        return Response("User was Updated", status=status.HTTP_200_OK)

