from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VoiceSerializer
from .models import Voice
import azure.cognitiveservices.speech as speechsdk
import wave
from .secret import voice_key
import time
import os
from django.core.mail import send_mail
from users.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


def speech_recognize_continuous(filename):
    recognized_str = ""
    speech_key, service_region = voice_key.SPEECH_KEY, "koreacentral"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    audio_config = speechsdk.audio.AudioConfig(filename=filename)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="ko-KR", audio_config=audio_config)
    result = speech_recognizer.recognize_once_async()
    result = result.get()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        recognized_str += result.text
    return recognized_str


class VoiceSTT(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VoiceSerializer(data=request.data)
        if serializer.is_valid():
            voice_file = request.data.get('voice')
            if not voice_file:
                return Response("voice file does not exist", status=status.HTTP_400_BAD_REQUEST)
            obj = wave.open(voice_file, 'r')
            audio = wave.open('test.wav', 'wb')
            audio.setnchannels(obj.getnchannels())
            audio.setnframes(obj.getnframes())
            audio.setsampwidth(obj.getsampwidth())
            audio.setframerate(obj.getframerate())
            blob = voice_file.read()
            audio.writeframes(blob)
            recognized_string = speech_recognize_continuous("test.wav")
            if os.path.isfile("test.wav"):
                os.remove("test.wav")
            send_mail(
                "[FINDME] 녹음본을 텍스트로 변환한 결과입니다.",
                recognized_string,
                'capstone4824@gmail.com',
                User.objects.filter(email=request.user.email).values_list('email', flat=True),
                fail_silently=False,
            )
            return Response(recognized_string, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

