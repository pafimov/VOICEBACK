from django.http import HttpResponse
from django.shortcuts import render
from django.templatetags.static import static
from .models import Detail, Word
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth.models import User
from .serializers import *
from .mail import Emailer

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'success' : True,
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    
emails = dict()

class SendCode(APIView):

    def post(self, request, *args, **kwargs):
        serializer = EmailCheck(data=request.data)
        if not serializer.is_valid():
            return Response({'message' :{'email' : ['Wrong email']}})
        emails[request.user.pk] = Emailer(serializer.validated_data['email'])
        emails[request.user.pk].go_send()
        return Response({
            'success' : True,})
    
class CheckCode(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get('code', -1)            
        if not request.user.pk in emails:
            return Response({'message' : {'email' : ['Not specified']}})
        a = emails[request.user.pk].check(code)
        if a == False:
            return Response({'message' : {'code' : ['Wrong code']}})
        return Response({
            'success' : True,
            'secret' : a})
    

class RegisterView(APIView):
    def post(self, request):
        user_serializer = RegistrationSerializer(data=request.data)
        if not request.user.pk in emails:
            return Response({'message' : {'email' : ['Not specified']}})
        if user_serializer.is_valid():
            secret = request.data.get('secret', '')
            if (not emails[request.user.pk].final_check(user_serializer.validated_data['email'], secret)):
                return Response({'success' : False})
            new_user = User.objects.create_user(user_serializer.validated_data['email'], user_serializer.validated_data['email'], user_serializer.validated_data['password'])
            new_detail = Detail(user=new_user)
            new_detail.save()
            token = str(Token.objects.get_or_create(user=new_user))
            return Response({'success' : True,
                             'token' : token})
        return Response({'message' : user_serializer.errors})

class GetUserName(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def post(self, request):
        user = request.user
        content = {
            'success' : True,
            'username' : user.username,
            'group' : user.detail.role
        }
        return Response(content)

def main_page(request):
    return render(request, 'test.html')

class get_videos(APIView):
    def post(self, request):
        word = request.POST.get('word', '')
        accent = request.POST.get('accent', '')
        print(word, end=' ')
        print(accent)
        videos = Word.objects.filter(word=word, accent=accent).order_by('pk')
        content = {'success' : True, 'data' : []}
        for video in videos:
            video.check_sentence_video()
            obj = {
                'sentence' : static(str(video.sentence_video)),
                'film_name' : video.film_name
            }
            content['data'].append(obj)
        return Response(content)
    

class get_audios(APIView):
    def post(self, request):
        word = request.POST.get('word', '')
        accent = request.POST.get('accent', '')
        print(word, end=' ')
        print(accent)
        videos = Word.objects.filter(word=word, accent=accent).order_by('pk')
        content = {'success' : True, 'data' : [], 'other' : []}
        for video in videos:
            video.check_word_audio()
            obj = {
                'word' : static(str(video.word_audio)),
            }
            content['data'].append(obj)
        other = Word.objects.filter(word__icontains=word, accent=accent).values_list("word", flat=True).distinct()
        if len(other) > 5:
            other = other[:5]
        print(other)
        for suggestion in other:
            if suggestion == word:
                continue
            content['other'].append(suggestion)
        return Response(content)

