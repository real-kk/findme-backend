from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
from .serializers import DiarySerializer
from django.core.files.images import ImageFile
from .models import Diary
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
            text = request.data['content'].encode("utf-8")
            # analyze sentiment
            credentials = service_account.Credentials.from_service_account_file(os.path.abspath('.') + '\\diary\\junctionx-3584b0288638.json')
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
            diary = Diary(title=request.data.get('title'), content=request.data.get('content'), client=request.user, create_date=datetime.now, sentiment_score=sentiment.score)
            diary.image.save('test.png', image)
            diary.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
