from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.core import serializers
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from  rest_framework.permissions import IsAuthenticated
from .models import Task
from django.core.files.storage import File
import json
from users.models import User
import requests

class TaskUpload(APIView):
        
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, **kwargs):
        if kwargs.get('id') is None:
            return Response('invalid request', status=status.HTTP_400_BAD_REQUEST)
        serializers = TaskSerializer(data=request.data)
        if serializers.is_valid():
            try : 
                task_id = kwargs.get('id')
                selected_task = Task.objects.get(id=task_id)
            except:
                return Response('task Not Founded',status= status.HTTP_404_NOT_FOUND)
            selected_task.video = request.data.get('video')
            selected_task.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):
            
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        task_id=request.GET.get('task_id',None)
        try:
            Task.objects.get(id=task_id)
            task = Task.objects.filter(id=task_id)
        except:
            return Response('Task Not Exist Error',status=status.HTTP_400_BAD_REQUEST)
        data=task.values('id','title','create_date','video')
        # for t in task:
        #     if t.video =="":
        #         print("hi") 제목만 반환하는 경우
        return Response(data, status=status.HTTP_200_OK)

class AddTaskQuestion(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskQuestionSerializer(data=request.data)
        if serializer.is_valid():
            client_email = request.data.get('client')
            client = User.objects.get(email=client_email)
            task = Task(question=request.data.get('question'), counselor=request.user, client=client)
            task.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        questions = Task.objects.filter(client=request.user)
        serializer = TaskQuestionSerializer(questions, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class VideoProcessing(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        if kwargs.get('id') is None:
            return Response('invalid request', status=status.HTTP_400_BAD_REQUEST)
        new_video = Task.objects.get(pk=kwargs.get("id"))
        url = 'https://processed-video-lambda.s3.ap-northeast-2.amazonaws.com/' + new_video.filename()
        response = requests.get(url)
        if str(response.status_code) == '200':
            return Response(url, status=status.HTTP_200_OK)
        return Response("Processed Video is not exist", status=status.HTTP_404_NOT_FOUND)
