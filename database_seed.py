import os
import sys

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
DATASET_PATH = os.getenv('DATASET_PATH')


def seed_exercises(filepath):
    exercises = pd.read_excel(filepath, sheet_name=None)
    existing_exercise_names = set(Exercise.objects.values_list('name', flat=True))
    for sheet_name, sheet in exercises.items():
        sheet = sheet.drop_duplicates(subset=['Exercise_Name'])

        for name, target_muscle, equipment in zip(sheet['Exercise_Name'], sheet['muscle_gp'], sheet['Equipment']):
            equipment = equipment if type(equipment) is not float else None  # nan values to None so NULL is in DB
            ex = Exercise(name=name, target_muscle=target_muscle, equipment=equipment)
            if ex.name not in existing_exercise_names:
                ex.save()


def update_exercises_url():
    ex_to_update = Exercise.objects.filter(youtube_url=None)
    for ex in ex_to_update:
        if ex.youtube_url is None:
            try:
                ex.youtube_url = get_youtube_video_url(ex.name, YT_API_KEY)
                ex.save()
            except Exception as e:
                print("Quotas exceeded for today! Exiting...")
                print(f"Error: {e}")
                sys.exit(1)


if __name__ == "__main__":
    update_exercises_url()
