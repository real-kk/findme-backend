from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
from .serializers import DiarySerializer, DiaryListSerializer, WholeContentSerializer
from django.core.files.images import ImageFile
from .models import Diary, DiaryWholeContent
import io
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from google.cloud import language_v1
from datetime import datetime
from google.oauth2 import service_account
import os 
class Text_extract_wordcloud(APIView):
    """
    감정일기 작성 및 워드클라우드 생성 API

    ---
    # /diaries/
    ## headers
        - Authorization : Token "key 값" [ex> Token 822a24a314dfbc387128d82af6b952191dd71651]
    ## body parameter
        - title : 감정일기 제목
        - content : 감정일기 내용
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = DiarySerializer(data=request.data)
        if serializer.is_valid():
            text = request.data['content'].encode('euc-kr').decode('euc-kr')
            # analyze sentiment
            credentials = service_account.Credentials.from_service_account_file(os.path.abspath('.') + '/diary/junctionx-3584b0288638.json')
            client = language_v1.LanguageServiceClient(credentials=credentials)
            document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
            sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
            # generate wordcloud
            okt = Okt()
            morphs = okt.pos(text)
            noun_adj_list = []
            for word, tag in morphs:
                if tag in ['Noun', 'Adjective']:
                    noun_adj_list.append(word)
            counts = Counter(noun_adj_list)
            tags = counts.most_common(10)
            wordcloud = WordCloud(font_path='/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf', background_color="white", width=300, height=300)
            cloud = wordcloud.generate_from_frequencies(dict(tags))
            plt.figure(figsize=(22, 22))
            plt.imshow(cloud, interpolation='lanczos')
            plt.axis('off')
            f = io.BytesIO()
            plt.savefig(f, format="png")
            image = ImageFile(f)
            # Diary Model 
            diary = Diary(title=request.data.get('title'), content=request.data.get('content'), client=request.user, create_date=datetime.now, sentiment_score=sentiment.score)
            diary.image.save('test.png', image)
            diary.save()
            # Whole Content Model Refresh
            try:
                pre_content = DiaryWholeContent.objects.get(client=request.user)
                pre_content.whole_content += text
                pre_content.save()
            except DiaryWholeContent.DoesNotExist:
                diary_whole_content = DiaryWholeContent(client=request.user, whole_content=request.data.get('content'))
                diary_whole_content.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        diary = Diary.objects.filter(client=request.user)
        serializer = DiaryListSerializer(diary, many=True)
        return Response(serializer.data)

class Whole_content_to_wordcloud(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            whole_content = DiaryWholeContent.objects.get(client=request.user)
        except DiaryWholeContent.DoesNotExist:
            whole_content = DiaryWholeContent(client=request.user, image=os.path.abspath('.') + '/diary/not_existing_diary.png')
            whole_content.save()
            serializer = WholeContentSerializer(whole_content)
            DiaryWholeContent.objects.filter(client=request.user)[0].delete()
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        # Generate whole wordcloud
        okt = Okt()
        morphs = okt.pos(whole_content.whole_content)
        noun_adj_list = []
        for word, tag in morphs:
            if tag in ['Noun', 'Adjective']:
                noun_adj_list.append(word)
        counts = Counter(noun_adj_list)
        tags = counts.most_common(10)
        wordcloud = WordCloud(font_path='/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf', background_color="white", width=300, height=300)
        cloud = wordcloud.generate_from_frequencies(dict(tags))
        plt.figure(figsize=(22, 22))
        plt.imshow(cloud, interpolation='lanczos')
        plt.axis('off')
        f = io.BytesIO()
        plt.savefig(f, format="png")
        image = ImageFile(f)
        whole_content.image.save('test.png', image)
        whole_content.save()
        serializer = WholeContentSerializer(whole_content)
        return Response(serializer.data)
