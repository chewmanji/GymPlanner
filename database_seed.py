import os
import django
import numpy as np

# Set the default Django settings module for the 'django' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GymPlanner.settings')

# Setup Django
django.setup()

import pandas as pd
from app.models import Exercise
from dotenv import load_dotenv
from app.youtube_utils import get_youtube_video_url

load_dotenv()
YT_API_KEY = os.getenv('YOUTUBE_API_KEY')


def seed_exercises_with_urls(filepath):
    exercises = pd.read_excel(filepath, sheet_name=None)
    for sheet_name, sheet in exercises.items():
        sheet = sheet.drop_duplicates(subset=['Exercise_Name'])

        for name, target_muscle, equipment in zip(sheet['Exercise_Name'], sheet['muscle_gp'], sheet['Equipment']):
            equipment = equipment if type(equipment) is not float else None  # nan values to None so NULL is in DB
            yt_url = get_youtube_video_url(name, YT_API_KEY)
            ex = Exercise(name=name, target_muscle=target_muscle, equipment=equipment, youtube_url=yt_url)

            ex.save()

def seed_exercises_with(filepath):
    exercises = pd.read_excel(filepath, sheet_name=None)
    existing_exercise_names = set(Exercise.objects.values_list('name', flat=True))
    for sheet_name, sheet in exercises.items():
        sheet = sheet.drop_duplicates(subset=['Exercise_Name'])

        for name, target_muscle, equipment in zip(sheet['Exercise_Name'], sheet['muscle_gp'], sheet['Equipment']):
            equipment = equipment if type(equipment) is not float else None  # nan values to None so NULL is in DB
            ex = Exercise(name=name, target_muscle=target_muscle, equipment=equipment)
            if ex.name not in existing_exercise_names:
                ex.save()



if __name__ == "__main__":
    #Exercise.objects.all().delete()
    #seed_exercises_with_urls("C:\\Users\\wojte\\PycharmProjects\\GymPlanner\\Gym Exercises Dataset.xlsx")
    seed_exercises_with("C:\\Users\\wojte\\PycharmProjects\\GymPlanner\\Gym Exercises Dataset.xlsx")
