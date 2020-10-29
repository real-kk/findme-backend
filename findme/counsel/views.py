from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.images import ImageFile
from .models import Counsel, CounselDate
from .serializer import CounselSerializer, CounselListSerializer, CounselDateSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from users.models import User
from datetime import datetime

class Counsel_application(APIView):
    """
    신청서 작성 API

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

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        selected_counselor_email= request.data.get("counselor")
        counselor = User.objects.get(email=selected_counselor_email)
        counsel = Counsel(time_table=request.data.get("time_table"), major=request.data.get("major"), client=request.user,counselor=counselor, create_date=datetime.now(),phone_number=request.data.get("phone_number"), student_number=request.data.get("student_number"), content=request.data.get("content"))
        serializer = CounselSerializer(counsel)
        if serializer.is_valid: 
            counsel.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        counsel = Counsel.objects.filter(client=request.user)
        serializer = CounselListSerializer(counsel, many=True)
        return Response(serializer.data)

class UpdateCounselForDate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = CounselDateSerializer(data=request.data)
        if serializer.is_valid():
            selected_client_email = request.data.get("client")
            client = User.objects.get(email=selected_client_email)
            counsel_date = CounselDate(counselor=request.user, client=client, counsel_date=request.data.get("counsel_date"))
            counsel_date.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
