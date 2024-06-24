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
    path('userexercises/', views.user_exercises, name='userexercise_list'),
    path('remove_userexercise_from_training/<int:training_id>/<int:userexercise_id>/',
         views.remove_userexercise_from_training, name='remove_userexercise_from_training'),
    path('create_exercise/<int:ex_id>/', views.CreateUserExercise.as_view(), name='create_userexercise'),
    path('update_exercise/<int:pk>/', views.UpdateUserExercise.as_view(), name='update_userexercise'),
    path('delete_exercise/<int:pk>/', views.DeleteUserExercise.as_view(), name='delete_userexercise'),
    path('exercises/<int:ex_id>/', views.exercise_detail, name='exercise_detail'),
    path('create_training/', views.CreateTraining.as_view(), name='create_training'),
    path('update_training/<int:pk>/', views.UpdateTraining.as_view(), name='update_training'),
    path('delete_training/<int:pk>/', views.DeleteTraining.as_view(), name='delete_training'),
    path('training_details/<int:training_id>', views.training_details, name='training_details'),
    path('plan_details/<int:plan_id>', views.plan_details, name='plan_details'),
    path('create_plan/', views.CreatePlan.as_view(), name='create_plan'),
    path('update_plan/<int:pk>/', views.UpdatePlan.as_view(), name='update_plan'),
    path('delete_plan/<int:pk>/', views.DeletePlan.as_view(), name='delete_plan'),
    path('remove_training_from_plan/<int:plan_id>/<int:training_id>', views.remove_training_from_plan,
         name='remove_training_from_plan')

]
