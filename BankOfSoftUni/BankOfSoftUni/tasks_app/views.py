from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from BankOfSoftUni.tasks_app.forms import CreateTargetsForm
from BankOfSoftUni.tasks_app.models import UserAnnualTargets


class CreateTargets(views.CreateView):
    form_class = CreateTargetsForm
    template_name = 'main/target_create.html'
    success_url = reverse_lazy('index')
