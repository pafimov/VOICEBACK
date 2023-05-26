import csv
from django.core.management.base import BaseCommand
from main.models import Word
import os

class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        path = options['file']
        video = options['video']
        if video == None:
            print("WHICH VIDEO??")
            return
        if not os.path.exists(path):
            print("PATH DOES NOT EXIST!!")
            return
        file = open(path)
        reader = csv.reader(file, delimiter=",", quotechar='"')
        next(reader, None)
        for row in reader:
            print(row)
            if Word.objects.filter(word=row[0]).count()>=5:
                continue
            new_word = Word(word = row[0], full_video=video, word_start = float(row[1]), word_end = float(row[2]),
                            sentence_start=float(row[3]), sentence_end=float(row[4]))
            new_word.save()

        file.close()


    def add_arguments(self, parser):
        parser.add_argument(nargs='?', type=str, dest="file")
        parser.add_argument(nargs='?', type=str, dest="video")