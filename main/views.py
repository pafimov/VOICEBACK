from django.http import HttpResponse
from django.shortcuts import render
from django.templatetags.static import static
from .models import Word
from rest_framework.views import APIView
from rest_framework.response import Response

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

