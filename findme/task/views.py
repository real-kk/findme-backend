from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.core import serializers
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from  rest_framework.permissions import IsAuthenticated
from .models import Task, TaskQuestion
from django.core.files.storage import File
import json
from users.models import User

class TaskUpload(APIView):
        
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializers=TaskSerializer(data=request.data)
        
        if serializers.is_valid():
            task = Task(video=request.data.get('video'),client=request.user)
            task.save()
            return Response(serializers.data, status= status.HTTP_201_CREATED)
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
            return Response('Task Not Exist Error',status=404)
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
            task_question = TaskQuestion(question=request.data.get('question'), counselor=request.user, client=client)
            task_question.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

