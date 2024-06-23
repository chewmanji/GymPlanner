from django.contrib import admin
from .models import Exercise, UserExercise, UserProfile, Plan, Training

# Register your models here.

admin.site.register(Exercise)
admin.site.register(UserExercise)
admin.site.register(UserProfile)
admin.site.register(Plan)
admin.site.register(Training)

