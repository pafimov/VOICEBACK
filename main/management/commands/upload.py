import csv
from django.core.management.base import BaseCommand
from main.models import Word
import os

class Command(BaseCommand):
    help = 'Write python manage.py [PATH TO CSV] [NAME OF FULL VIDEO FROM STATIC] [ACCENT] [NMAE OF FILM]'

    def handle(self, *args, **options):
        path = options['file']
        video = options['video']
        accent = options['accent']
        film_name = options['film_name']
        if path == None:
            print("WHICH PATH??")
            return
        if video == None:
            print("WHICH VIDEO??")
            return
        if accent == None:
            print("WHICH ACCENT??")
            return
        if film_name == None:
            print("NAME OF FILM??")
            return
        if not os.path.exists(path):
            print("PATH DOES NOT EXIST!!")
            return
        film_name = ' '.join(film_name)
        file = open(path)
        reader = csv.reader(file, delimiter=",", quotechar='"')
        next(reader, None)
        for row in reader:
            print(row)
            if Word.objects.filter(word=row[0]).count()>=3:
                continue
            new_word = Word(word = row[0], full_video=video, word_start = float(row[1]), word_end = float(row[2]),
                            sentence_start=float(row[3]), sentence_end=float(row[4]), accent=accent, film_name=film_name)
            new_word.save()

        file.close()


    def add_arguments(self, parser):
        parser.add_argument(nargs='?', type=str, dest="file")
        parser.add_argument(nargs='?', type=str, dest="video")
        parser.add_argument(nargs='?', type=str, dest="accent")
        parser.add_argument('--film_name', nargs='+', type=str, dest="film_name")