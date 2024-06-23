from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('trainings/', views.trainings, name='trainings'),
    path('plans/', views.plans, name='plans'),
    path('exercises', views.exercises, name='exercise_list'),
    path('create_exercise/<int:ex_id>/', views.CreateUserExercise.as_view(), name='create_userexercise'),
    path('update_exercise/<int:pk>/', views.UpdateUserExercise.as_view(), name='update_userexercise'),
    path('exercises/<int:ex_id>/', views.exercise_detail, name='exercise_detail'),
    path('create_training/', views.CreateTraining.as_view(), name='create_training'),
    path('update_training/<int:pk>/', views.UpdateTraining.as_view(), name='update_training'),
    path('training_details/<int:training_id>', views.training_details, name='training_details'),
    path('create_plan/', views.CreatePlan.as_view(), name='create_plan'),
    path('plan_details/<int:plan_id>', views.plan_details, name='plan_details'),

]
