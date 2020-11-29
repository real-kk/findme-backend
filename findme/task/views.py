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
import matplotlib.pyplot as plt
import io
from django.core.files.images import ImageFile
from datetime import datetime


def create_sentiment_graph_result(sentiments):
    length = len(sentiments)
    sentiment_scores = [[] for _ in range(8)]
    sentiment_type = ["anger", 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']
    colors = ['red', 'maroon', 'orange', 'black', 'lime', 'indigo', 'cyan', 'yellow']
    for second in sentiments:
        sentiment_values = list(map(str, sentiments.get(second).split('\n')))[:-1]
        for idx, each_value in enumerate(sentiment_values):
            sentiment_scores[idx].append(float(each_value.split(':')[1]))
    plt.figure(figsize=(8,8))
    x = list(sentiments.keys())
    for i in range(8):
        plt.plot(x, sentiment_scores[i], color=colors[i], label=sentiment_type[i])
    plt.legend()
    plt.axis([1, 7, 0, 1])
    plt.xlabel('second')
    plt.ylabel('sentiment_score')
    fig = plt.gcf()
    file_io = io.BytesIO()
    fig.savefig(file_io, format="png")
    graph_image = ImageFile(file_io)
    return graph_image

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
            selected_task.video.name = str(kwargs.get('uuid')) + '.mp4'
            selected_task.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):
            
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,**kwargs):
        if request.user.user_type != '1':
            return Response("Only Counselor can delete Task", status=status.HTTP_403_FORBIDDEN)

        if kwargs.get('id') is None:
            return Response('invalid request', status=status.HTTP_400_BAD_REQUEST)
        else:
            task_id = kwargs.get('id')
            try:
                task = Task.objects.get(id=task_id)
                task.delete()
            except:
                return Response("Task not founded", status=status.HTTP_400_BAD_REQUEST)

            return Response("Task was deleted", status=status.HTTP_200_OK)

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

class TaskQuestionForCounselor(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client_email = request.GET.get('client')
        client = User.objects.get(email=client_email)
        questions = Task.objects.filter(client=client, counselor=request.user)
        serializer = TaskQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VideoProcessing(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        if kwargs.get('id') is None:
            return Response('invalid request', status=status.HTTP_400_BAD_REQUEST)
        new_video = Task.objects.get(pk=kwargs.get("id"))
        print(new_video.video.name)
        url = 'https://processed-video-lambda.s3.ap-northeast-2.amazonaws.com/' + str(new_video.video.name)
        response = requests.get(url)
        if str(response.status_code) == '200':
            return Response(url, status=status.HTTP_200_OK)
        return Response("Processed Video is not exist", status=status.HTTP_404_NOT_FOUND)


class GetSentiment(APIView):
    def post(self, request):
        sentiments = request.data.get("sentiments")
        filename = request.data.get("key")
        print(filename)
        task = Task.objects.filter(video=filename)[0]
        sentiment_graph = create_sentiment_graph_result(sentiments)
        task.graph.save("sentiment_graph" + datetime.now().strftime('%Y-%m-%d_%H%M%S') + ".png", sentiment_graph)
        task.save()
        plt.cla()
        return Response(request.data, status=status.HTTP_200_OK)

class MakeSentimentLinegraph(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        task = Task.objects.get(client=request.user)
        serializer = SentimentGraphSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def get(self, request):
        client_email = request.GET.get('client')
        client = User.objects.get(email=client_email)
        task = create_sentiment_graph_result(request, client)
        serializer = SentimentGraphSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

