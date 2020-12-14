from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.images import ImageFile
from .models import Counsel, RegisterCounselDate
from .serializer import CounselSerializer, CounselListSerializer,CounselCounselorSerializer, CounselDateSerializer, CounselClientSerializer, CounselPhotoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from users.models import User
from django.utils.timezone import now
import json
from datetime import datetime

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
        counsel = Counsel(major=request.data.get("major"), client=request.user,counselor=counselor, create_date=now(),phone_number=request.data.get("phone_number"), student_number=request.data.get("student_number"), content=request.data.get("content"))
        serializer = CounselSerializer(counsel)
        if serializer.is_valid: 
            counsel.save()
            return Response((serializer.data, counsel.pk), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        """
        신청서 조회

        ---
        # /counsels/
        ## headers
            - Authorization : Token "key 값" [ex> Token 822a24a314dfbc387128d82af6b952191dd71651]
        """
        if request.user.user_type=="1":
            counsel = Counsel.objects.filter(counselor_id=request.user.id)

        elif request.user.user_type=="0":
            counsel = Counsel.objects.filter(client_id=request.user.id)
        serializer = CounselListSerializer(counsel, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        """
        신청서 삭제

        ---
        # /counsels/<id:int>/?counsel_date_id=
        ## headers
            - Authorization : Token "key 값" [ex> Token 822a24a314dfbc387128d82af6b952191dd71651]
        ## query parameter
            - counsel_date_id : 신청 수락시 상담 id, 신청 보류시 -1

        """
        if kwargs.get('id') is None:
            return Response('invalid request', status=status.HTTP_400_BAD_REQUEST)
        else:

            counsel_id = kwargs.get('id')
            try:
                counsel_obj = Counsel.objects.get(id=counsel_id)
                

            except:
                return Response("Counsel not found", status=status.HTTP_400_BAD_REQUEST)

            if str(counsel_obj.counselor)== str(request.user.email):
                #parameter로 받아온 counseldate 의 id값으로 해당 counseldate 에 데이터 넣어주기
                if request.query_params.get('counsel_date_id')=='-1':
                    counsel_obj.delete()
                    return Response("Counsel was deleted", status=status.HTTP_200_OK)

                else:
                    counseldate = RegisterCounselDate.objects.get(id= int(request.query_params.get('counsel_date_id')))
                    counseldate.counselor= counsel_obj.counselor
                    counseldate.client=counsel_obj.client
                    counseldate.major=counsel_obj.major
                    counseldate.student_number=counsel_obj.student_number
                    counseldate.phone_number=counsel_obj.phone_number
                    counseldate.time_table=counsel_obj.time_table
                    counseldate.content=counsel_obj.content
                    counseldate.save()
                    counsel_obj.delete()
                    return Response("Counsel was deleted", status=status.HTTP_200_OK)

            
            else:
                return Response("Can only Delete your own counsel applications",status=status.HTTP_403_FORBIDDEN)

    def put(self, request, **kwargs):
        """
        신청서 수정

        ---
        # /counsels/<id:int>/
        ## headers
            - Authorization : Token "key 값" [ex> Token 822a24a314dfbc387128d82af6b952191dd71651]
        """
        if kwargs.get('id') is None:
            return Response('invalid request', status=status.HTTP_400_BAD_REQUEST)
        else:
            counsel_id = kwargs.get('id')
            try:
                counsel_obj = Counsel.objects.get(id=counsel_id)
            except:
                return Response("Counsel not found", status=status.HTTP_400_BAD_REQUEST)

            if str(counsel_obj.client)== str(request.user.email):
                selected_counselor_email= request.data.get("counselor")
                counselor = User.objects.get(email=selected_counselor_email)
                counsel_obj.counselor=counselor

                counsel_obj.content = request.data.get("content")
                counsel_obj.phone_number=request.data.get("phone_number")
                counsel_obj.student_number=request.data.get("student_number")
                counsel_obj.major=request.data.get("major")
                counsel_obj.time_table = request.data.get("time_table")

                counsel_obj.save()
                return Response("Counsel was updated", status=status.HTTP_200_OK)

            else:
                return Response("Can only Modify your own counsel application",status=status.HTTP_403_FORBIDDEN)
        
        
        counsel = Counsel(major=request.data.get("major"), client=request.user,counselor=counselor, create_date=now(),phone_number=request.data.get("phone_number"), student_number=request.data.get("student_number"), content=request.data.get("content"))
        serializer = CounselSerializer(counsel)
        if serializer.is_valid: 
            counsel.save()
            return Response((serializer.data, counsel.pk), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CounselPhoto(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):

        if kwargs.get('id') is None:
            return Response('invalid request', status=status.HTTP_400_BAD_REQUEST)
        serializer = CounselPhotoSerializer(data=request.data)

        if serializer.is_valid():
            counsel = Counsel.objects.get(pk=kwargs.get("id"))
            time_table = request.data.get("time_table")
            counsel.time_table.save("time_table" + datetime.now().strftime('%Y-%m-%d_%H%M%S') + ".png", time_table)
            counsel.save()
            return Response("Counsel time table was updated", status=status.HTTP_201_CREATED)
        import pprint
        pprint.pprint(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            counsel_date1= RegisterCounselDate.objects.create(counselor=request.user, client=client)
            counsel_date_id = str(counsel_date1)[28:-1]
            return Response(data={"id":counsel_date_id} ,status=status.HTTP_201_CREATED)
        import pprint
        pprint.pprint(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        """
        등록된 상담 조회
        
        ---
        # /counsels/date/
        ## headers
            - Authorization : Token
        """
        if request.user.user_type=="1":
            clients = RegisterCounselDate.objects.filter(counselor=request.user)
            if not clients.exists():
                return Response('Registered counsel does not exist',status=status.HTTP_200_OK)
            serializer = CounselClientSerializer(clients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            counselor = RegisterCounselDate.objects.filter(client=request.user)
            if not counselor.exists():
                 return Response('Registered counsel does not exist',status=status.HTTP_200_OK)
            serializer = CounselCounselorSerializer(counselor, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
    
    def delete(self, request,**kwargs):
        """
        등록된 상담 삭제
        
        ---
        # /counsels/date/<id:int>/
        ## headers
            - Authorization : Token
        """
        if kwargs.get('id') is None:
                return Response('invalid request', status=status.HTTP_400_BAD_REQUEST)
        else:
            registered_counsel_id = kwargs.get('id')
            try:
                registered_counsel_obj = RegisterCounselDate.objects.get(id=registered_counsel_id)
            except:
                return Response("Registered Counsel not found", status=status.HTTP_400_BAD_REQUEST)
            if str(registered_counsel_obj.client)== str(request.user.email):
                registered_counsel_obj.delete()
                return Response("Registered Counsel was deleted", status=status.HTTP_200_OK)
            else:
                return Response("Can only Delete your own registered Counsel",status=status.HTTP_403_FORBIDDEN)
