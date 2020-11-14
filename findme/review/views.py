from django.shortcuts import render
from .serializers import ReviewSerializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from datetime import datetime
from .models import Review
from django.forms.models import model_to_dict

class Review_upload(APIView):
 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        리뷰 생성

        ---
        # /reviews/
        ## headers
            - Authorization : Token "key 값" 
        ## body parameter
            - counselor : 상담사 user
            - client : 내담자 user
            - content : 후기 내용

        """

        selected_counselor_email= request.data.get("counselor")
        counselor = User.objects.get(email=selected_counselor_email)
        create_date= request.data.get("create_date")
        content= request.data.get("content")
        review = Review(client=request.user,counselor=counselor,create_date=datetime.now(),content=content)
        print(request.user.username, counselor.username)
        serializer=ReviewSerializer(review)
        if serializer.is_valid:

            review.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        리뷰 수정

        ---
        # /reviews/
        ## headers
            - Authorization : Token "key 값" 
        ## body parameter
            - review_id : 후기 id 값
            - content : 후기 내용

        """

        selected_counselor_email= request.data.get("counselor")
        selected_review = Review.objects.get(id=request.data.get("review_id"))
        counselor = User.objects.get(email=selected_counselor_email)
        create_date= request.data.get("create_date")
        content= request.data.get("content")

        review = Review(client=request.user,counselor=counselor,create_date=datetime.now(),content=content)
        serializer=ReviewSerializer(data={'client': request.user, 'counselor':counselor ,'create_date':datetime.now(),'content':content  })
        if serializer.is_valid():
            review.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
