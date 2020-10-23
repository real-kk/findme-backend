from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
from .serializers import DiarySerializer

class Text_extract_wordcloud(APIView):
    def post(self, request):
        serializer = DiarySerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            text = request.data['content'].encode("utf-8")
            okt = Okt()
            morphs = okt.pos(text)
            noun_adj_list = []
            for word, tag in morphs:
                if tag in ['Noun', 'Adjective']:
                    noun_adj_list.append(word)
            counts = Counter(noun_adj_list)
            tags = counts.most_common(10)
            wordcloud = WordCloud(font_path='NanumGothic-Regular.ttf', background_color="white", width=300, height=300)
            cloud = wordcloud.generate_from_frequencies(dict(tags))
            plt.figure(figsize=(22, 22))
            plt.imshow(cloud, interpolation='lanczos')
            plt.axis('off')
            plt.savefig('test_wordcloud.png')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        