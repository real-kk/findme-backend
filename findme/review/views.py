from django.shortcuts import render
from .serializers import ReviewSerializer,ReviewListSerializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from datetime import datetime
from .models import Review
from django.forms.models import model_to_dict
import json

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
        content= request.data.get("content")
        review = Review(client=request.user,counselor=counselor,create_date=datetime.now(),content=content)
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
        try:
            selected_review = Review.objects.get(id=request.data.get("review_id"))
        except : 
            return Response('Review not exist' , status=status.HTTP_400_BAD_REQUEST)
        content= request.data.get("content")
        selected_review.content =content
        try:
            selected_review.save()
        except : 
            return Response( 'Review updated failed' ,status=status.HTTP_400_BAD_REQUEST)

        return Response( 'Review updated success' ,status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        """
        리뷰 삭제

        ---
        # /reviews/<id:int>/
        ## headers
            - Authorization : Token "key 값" [ex> Token 822a24a314dfbc387128d82af6b952191dd71651]
        """
        if kwargs.get('id') is None:
            return Response('invalid request', status=status.HTTP_400_BAD_REQUEST)
        else:
            review_id = kwargs.get('id')
            try:
                review_obj = Review.objects.get(id=review_id)
                review_obj.delete()
                return Response("Review was deleted", status=status.HTTP_200_OK)
            except:
                return Response("Review not Found", status=status.HTTP_400_BAD_REQUEST)


class Review_get_by_counselor(APIView):
    def get(self, request,**kwargs):
        """
        특정 상담사의 리뷰 조회

        ---
        # /reviews/counselors/<int:id>/
        ## headers
            - Authorization : Token "key 값" 
        """
        if kwargs.get('id') is None:
            return Response('invalid request', status=status.HTTP_400_BAD_REQUEST)
        else:
            counselor = User.objects.get(id=kwargs.get('id'))
            review = Review.objects.filter(counselor=counselor)
            serializer = ReviewListSerializer(review, many=True)
            
            return Response(serializer.data,status=status.HTTP_200_OK)

class Review_get_by_client(APIView):
    def get(self, request,**kwargs):
        """
        특정 내담자의 리뷰 조회

        ---
        # /reviews/clients/<id : int>
        ## headers
            - Authorization : Token "key 값" 
        """
        if kwargs.get('id') is None:
            return Response('invalid request', status=status.HTTP_400_BAD_REQUEST)
        else:
            client = User.objects.get(id=kwargs.get('id'))
            review = Review.objects.filter(client=client)
            serializer = ReviewListSerializer(review, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)

