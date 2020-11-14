from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wordcloud import WordCloud
from konlpy.tag import Mecab
from collections import Counter
import matplotlib.pyplot as plt
from .serializers import DiarySerializer, DiaryListSerializer, WholeContentSerializer, LineGraphSerializer
from django.core.files.images import ImageFile
from .models import Diary, DiaryWholeContent, LineGraph
import io
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from google.cloud import language_v1
from datetime import datetime
from google.oauth2 import service_account
import os
import re
from users.models import User

def make_wordcloud(text):
    mecab = Mecab()
    text = re.compile('[|ㄱ-ㅎ|ㅏ-ㅣ]+').sub("", text)
    morphs = mecab.pos(text)
    noun_adj_list = []
    for word, tag in morphs:
        if tag in ['VA', 'NNG', 'NNP', 'NNB', 'NNBC', 'NR', 'NP'] and len(word) > 1:
            noun_adj_list.append(word)
    counts = Counter(noun_adj_list)
    tags = counts.most_common(10)
    wordcloud = WordCloud(font_path='/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf', background_color="white", width=300, height=300)
    cloud = wordcloud.generate_from_frequencies(dict(tags))
    plt.figure(figsize=(22, 22))
    plt.imshow(cloud, interpolation='lanczos')
    plt.axis('off')
    f = io.BytesIO()
    plt.savefig(f, format='png')
    plt.show()
    image = ImageFile(f)
    return image

def create_wordcloud_result(request, user):
    try:
        whole_content = DiaryWholeContent.objects.get(client=user)
    except DiaryWholeContent.DoesNotExist:
        whole_content = DiaryWholeContent(client=user, image=os.path.abspath('.') + '/diary/not_existing_diary.png')
        whole_content.save()
        serializer = WholeContentSerializer(whole_content)
        DiaryWholeContent.objects.filter(client=user)[0].delete()
        return ("400", serializer.data)
    if whole_content.renew_flag:
        image = whole_content.image
    else:
        image = make_wordcloud(whole_content.whole_content)
        whole_content.renew_flag = True
    whole_content.image.save('wordcloud' + datetime.now().strftime('%Y-%m-%d_%H%M%S') + '.png', image)
    whole_content.save()
    serializer = WholeContentSerializer(whole_content)
    return ("200", serializer.data)

def create_linegraph_result(request, user):
    scores = [score.get("sentiment_score", -1) for score in Diary.objects.filter(client=user).values("sentiment_score")]
    plt.figure(figsize=(8,8))
    if len(scores) == 1:
        x = [x_value for x_value in range(1, len(scores) + 1)]
        plt.plot(x, scores, 'ro')
    elif len(scores) < 7:
        x = [x_value for x_value in range(1, len(scores) + 1)]
        plt.plot(x, scores, 'r')
    else:
        x = [x_value for x_value in range(1, 8)]
        plt.plot(x, scores[-7:], 'r')
    plt.axis([1, 7, 0, 1])
    fig = plt.gcf()
    file_io = io.BytesIO()
    fig.savefig(file_io, format="png")
    graph_image = ImageFile(file_io)
    try:
        line_graph = LineGraph.objects.get(client=user)
    except LineGraph.DoesNotExist:
        line_graph = LineGraph(client=user)
    line_graph.line_graph.save("line_graph" + datetime.now().strftime('%Y-%m-%d_%H%M%S') + ".png", graph_image)
    line_graph.save()
    plt.cla()
    serializer = LineGraphSerializer(line_graph)
    return serializer.data

class Text_extract_wordcloud(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        감정일기 작성

        ---
        # /diaries/
        ## headers
            - Authorization : Token "key 값" [ex> Token 822a24a314dfbc387128d82af6b952191dd71651]
        ## body parameter
            - title : 감정일기 제목
            - content : 감정일기 내용
        """
        serializer = DiarySerializer(data=request.data)
        if serializer.is_valid():
            text = request.data['content'].encode('euc-kr').decode('euc-kr')
            # analyze sentiment
            credentials = service_account.Credentials.from_service_account_file(os.path.abspath('.') + '/diary/capstone-ed11e4ac6a67.json')
            client = language_v1.LanguageServiceClient(credentials=credentials)
            document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
            sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
            # Diary Model 
            diary = Diary(title=request.data.get('title'), content=request.data.get('content'), client=request.user, create_date=datetime.now(), sentiment_score=sentiment.score)
            diary.save()
            # Whole Content Model Refresh
            try:
                pre_content = DiaryWholeContent.objects.get(client=request.user)
                pre_content.whole_content += text
                pre_content.renew_flag = False
                pre_content.save()
            except DiaryWholeContent.DoesNotExist:
                diary_whole_content = DiaryWholeContent(client=request.user, whole_content=request.data.get('content'), renew_flag=False)
                diary_whole_content.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        """
        감정일기 조회

        ---
        # /diaries/
        ## headers
            - Authorization : Token "key 값" 
        """
        diary = Diary.objects.filter(client=request.user)
        serializer = DiaryListSerializer(diary, many=True)
        return Response(serializer.data)
    
    def delete(self,request):
        """
        감정일기 삭제

        ---
        # /diaries/
        ## headers
            - Authorization : Token "key 값"

        ## parameter
            - id : Diary id 값 
        """
        id = request.GET.get("id")
        queryset = Diary.objects.get(id=id)
        try:
            queryset.delete()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class Whole_content_to_wordcloud(APIView):
    """
    워드클라우드 생성

    ---
    # /whole_content/
    ## headers
        - Authorization : Token "key 값" 
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        exist_status, data = create_wordcloud_result(request, request.user)
        if exist_status == '200':
            return Response(data)
        return Response(data, status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        client_email = request.GET.get('client')
        client = User.objects.get(email=client_email)
        exist_status, data = create_wordcloud_result(request, client)
        if exist_status == '200':
            return Response(data)
        return Response(data, status.HTTP_400_BAD_REQUEST) 

class Text_extract_linegraph(APIView):
    """
    꺾은선그래프 생성

    ---
    # /linegraph
    ## headers
        - Authorization : Token "key 값" 
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = create_linegraph_result(request, request.user)
        return Response(data)
        
    def get(self, request):
        client_email = request.GET.get('client')
        client = User.objects.get(email=client_email)
        data = create_linegraph_result(request, client)
        return Response(data)

