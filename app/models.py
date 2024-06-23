from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    genders = [("M", "Male"), ("F", "Female")]
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=genders, null=True, blank=True)

    def __str__(self):
        return self.user.email


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    target_muscle = models.CharField(max_length=100)
    equipment = models.CharField(null=True, max_length=100)
    youtube_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=50)
    goals = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} | {self.start_date}"


class Training(models.Model):
    trainingTypes = [('FBW', 'FBW'),
                     ('Push', 'Push'),
                     ('Pull', 'Pull'),
                     ('Upper', 'Upper'),
                     ('Lower', 'Lower'),
                     ('Custom', 'Custom')]
    days = [(1, 'Monday'),
            (2, 'Tuesday'),
            (3, 'Wednesday'),
            (4, 'Thursday'),
            (5, 'Friday'),
            (6, 'Saturday'),
            (7, 'Sunday')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    weekday = models.IntegerField(blank=True, choices=days)
    type = models.CharField(blank=True, max_length=10, choices=trainingTypes)

    def __str__(self):
        return f"{self.name}"


class UserExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE, null=True, blank=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    setsNumber = models.IntegerField()
    repsNumber = models.IntegerField()
    tempo = models.CharField(max_length=10, null=True, blank=True)
    weight = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=3)
    notes = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"UserExercise: {self.exercise.name}, User: {self.user.email}"


class ExerciseProgress(models.Model):
    user_exercise = models.ForeignKey(UserExercise, on_delete=models.CASCADE)
    date = models.DateField()
    actual_sets = models.IntegerField()
    actual_reps = models.IntegerField()
    actual_weight = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=3)

    def __str__(self):
        return f"ExerciseProgress: {self.user_exercise.exercise.name}, User: {self.user_exercise.user.email}, Date: {self.date}"
