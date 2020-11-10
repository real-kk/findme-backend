from django.shortcuts import render
from .serializers import ReviewSerializer
class Review(APIView):
 
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

        serializer=ReviewSerializer(request.data)
        if serializer.is_valid():

            selected_counselor_email= request.data.get("counselor")
            counselor = User.objects.get(email=selected_counselor_email)
            create_date= request.data.get("create_date")
            content= request.data.get("content")

            review = Review(client=request.user,counselor=counselor,create_date=datetime.now(),content=content)
            review.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
