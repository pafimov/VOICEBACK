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
        print(word)
        videos = Word.objects.filter(word=word)
        content = {'success' : True, 'data' : []}
        for video in videos:
            video.check_all()
            obj = {
                'sentence' : static(str(video.sentence_video)),
                'word' : static(str(video.word_audio)),
            }
            content['data'].append(obj)
        return Response(content)

