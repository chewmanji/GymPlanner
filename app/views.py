from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Exercise, UserExercise, Training, Plan
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy


def home(request):
    return render(request, 'app/home.html')


def login(request):
    return render(request, "app/login.html")


def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def profile(request):
    return render(request, 'app/profile.html')


@login_required
def user_exercises(request):
    user_exercises = UserExercise.objects.filter(user=request.user)
    return render(request, 'app/userexercise_list.html', {'user_exercises': user_exercises})


@login_required
def trainings(request):
    trainings = Training.objects.filter(user=request.user)
    return render(request, 'app/trainings.html', {"trainings": trainings})


@login_required
def training_details(request, training_id):
    training = get_object_or_404(Training, pk=training_id)
    if request.user != training.user:
        return HttpResponseForbidden("You do not have permission to view this training.")
    user_exercises = UserExercise.objects.filter(training=training_id)
    context = {"training": training, "user_exercises": user_exercises}
    return render(request, 'app/training_details.html', context)


def remove_userexercise_from_training(request, training_id, userexercise_id):
    user_exercise = get_object_or_404(UserExercise, pk=userexercise_id)
    if request.user != user_exercise.user:
        return HttpResponseForbidden("You do not have permission to remove this exercise.")

    user_exercise.training = None
    user_exercise.save()
    return training_details(request, training_id)


@login_required
def plan_details(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)
    if request.user != plan.user:
        return HttpResponseForbidden("You do not have permission to view this plan.")
    trainings = Training.objects.filter(plan=plan_id)
    context = {"trainings": trainings, "plan": plan}
    return render(request, 'app/plan_details.html', context)


def remove_training_from_plan(request, plan_id, training_id):
    training = get_object_or_404(Training, pk=training_id)
    if request.user != training.user:
        return HttpResponseForbidden("You do not have permission to remove this training.")
    training.plan = None
    training.save()
    return plan_details(request, plan_id)


@login_required
def plans(request):
    plans = Plan.objects.filter(user=request.user)
    return render(request, 'app/plans.html', {"plans": plans})


def exercises(request):
    exercises_list = Exercise.objects.all()
    context = {
        'exercises': exercises_list,
    }
    return render(request, 'app/exercise_list.html', context)


def exercise_detail(request, ex_id):
    exercise = get_object_or_404(Exercise, pk=ex_id)
    return render(request, "app/exercise_detail.html", {"exercise": exercise})


class CreateUserExercise(LoginRequiredMixin, CreateView):
    model = UserExercise
    success_url = reverse_lazy('app:exercise_list')
    fields = ['training', 'setsNumber', 'repsNumber', 'tempo', 'weight', 'notes']

    def get_initial(self):
        initial = super().get_initial()
        exercise_id = self.kwargs.get('exercise_id')
        if exercise_id:
            initial['exercise'] = Exercise.objects.get(id=exercise_id)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exercise_id = self.kwargs.get('ex_id')
        if exercise_id:
            context['exercise'] = Exercise.objects.get(id=exercise_id)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.exercise_id = self.kwargs.get('ex_id')
        messages.success(self.request, 'Exercise added successfully!')
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['training'].queryset = Training.objects.filter(user=self.request.user)
        return form


class UpdateUserExercise(LoginRequiredMixin, UpdateView):
    model = UserExercise
    fields = ['training', 'setsNumber', 'repsNumber', 'tempo', 'weight', 'notes']
    success_url = reverse_lazy('app:trainings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userexercise_id = self.kwargs.get('pk')
        if userexercise_id:
            context['exercise'] = UserExercise.objects.get(id=userexercise_id).exercise
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.exercise_id = UserExercise.objects.get(id=self.kwargs.get('pk')).exercise.id
        messages.success(self.request, 'Exercise edited successfully!')
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['training'].queryset = Training.objects.filter(user=self.request.user)
        return form


class DeleteUserExercise(LoginRequiredMixin, DeleteView):
    model = UserExercise
    success_url = reverse_lazy('app:userexercise_list')


class CreateTraining(LoginRequiredMixin, CreateView):
    model = Training
    success_url = reverse_lazy('app:trainings')
    fields = ['name', 'weekday', 'type', 'plan']

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Training created successfully!')
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['plan'].queryset = Plan.objects.filter(user=self.request.user)
        return form

    def get_initial(self):
        initial = super().get_initial()
        training_id = self.kwargs.get('training_id')
        if training_id:
            initial['training'] = get_object_or_404(Training, id=training_id)
        return initial


class UpdateTraining(LoginRequiredMixin, UpdateView):
    model = Training
    success_url = reverse_lazy('app:trainings')
    fields = ['name', 'weekday', 'type', 'plan']

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Training created successfully!')
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['plan'].queryset = Plan.objects.filter(user=self.request.user)
        return form

    def get_initial(self):
        initial = super().get_initial()
        training_id = self.kwargs.get('training_id')
        if training_id:
            initial['training'] = get_object_or_404(Training, id=training_id)
        return initial


class DeleteTraining(LoginRequiredMixin, DeleteView):
    model = Training

    def get_success_url(self):
        plan_id = self.object.plan_id
        if plan_id:
            return reverse_lazy('app:plan_details', kwargs={'plan_id': plan_id})
        else:
            return reverse_lazy('app:trainings')


class CreatePlan(LoginRequiredMixin, CreateView):
    model = Plan
    success_url = reverse_lazy('app:plans')
    fields = ['name', 'start_date', 'end_date', 'goals']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget.attrs.update({
            'placeholder': 'Month/Day/Year'
        })
        form.fields['end_date'].widget.attrs.update({
            'placeholder': 'Month/Day/Year'
        })
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Plan created successfully!')
        return super().form_valid(form)


class UpdatePlan(LoginRequiredMixin, UpdateView):
    model = Plan
    success_url = reverse_lazy('app:plans')
    fields = ['name', 'start_date', 'end_date', 'goals']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget.attrs.update({
            'placeholder': 'Month/Day/Year'
        })
        form.fields['end_date'].widget.attrs.update({
            'placeholder': 'Month/Day/Year'
        })
        return form

    def get_initial(self):
        initial = super().get_initial()
        plan_id = self.kwargs.get('plan_id')
        if plan_id:
            initial['plan'] = get_object_or_404(Training, id=plan_id)
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Plan created successfully!')
        return super().form_valid(form)


class DeletePlan(LoginRequiredMixin, DeleteView):
    model = Plan
    success_url = reverse_lazy('app:plans')
