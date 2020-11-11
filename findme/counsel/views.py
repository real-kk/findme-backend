from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.images import ImageFile
from .models import Counsel, RegisterCounselDate
from .serializer import CounselSerializer, CounselListSerializer, CounselDateSerializer, CounselClientSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from users.models import User
from django.utils.timezone import now

class Counsel_application(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        신청서 작성

        ---
        # /counsels/
        ## headers
            - Authorization : Token "key 값" [ex> Token 822a24a314dfbc387128d82af6b952191dd71651]
        ## body parameter
            - counselor : 상담사 user
            - major : 전공
            - student_number : 학번
            - phone_number : 핸드폰 번호
            - time_table : 시간표
            - content : 상담 신청 이유
        """
        selected_counselor_email= request.data.get("counselor")
        counselor = User.objects.get(email=selected_counselor_email)
        counsel = Counsel(time_table=request.data.get("time_table"), major=request.data.get("major"), client=request.user,counselor=counselor, create_date=now(),phone_number=request.data.get("phone_number"), student_number=request.data.get("student_number"), content=request.data.get("content"))
        serializer = CounselSerializer(counsel)
        if serializer.is_valid: 
            counsel.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        """
        신청서 조회

        ---
        # /counsels/
        ## headers
            - Authorization : Token "key 값" [ex> Token 822a24a314dfbc387128d82af6b952191dd71651]
        """
        counsel = Counsel.objects.filter(counselor=request.user)
        serializer = CounselListSerializer(counsel, many=True)
        return Response(serializer.data)

class CounselDate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        상담 등록

        ---
        # /counsels/date/
        ## headers
            - Authorization : Token
        ## body parameter
            - client : 내담자 이메일 [ex> capstone4824@gmail.com]
            - counsel_date : 상담 날짜 [ex> 2020-10-30T20:38:59Z]
        """
        serializer = CounselDateSerializer(data=request.data)
        if serializer.is_valid():
            selected_client_email = request.data.get("client")
            client = User.objects.get(email=selected_client_email)
            counsel_date = RegisterCounselDate(counselor=request.user, client=client, counsel_date=request.data.get("counsel_date"))
            counsel_date.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        """
        등록된 상담 조회
        
        ---
        # /counsels/date/
        ## headers
            - Authorization : Token
        """
        clients = RegisterCounselDate.objects.filter(counselor=request.user)
        serializer = CounselClientSerializer(clients, many=True)
        return Response(serializer.data)
        

