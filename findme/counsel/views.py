from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.images import ImageFile
from .models import Counsel
from .serializer import CounselSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from users.models import User
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
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = CounselSerializer(data=request.data)
        if serializer.is_valid():
            print(User.objects.all())
            counsel = Counsel()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
