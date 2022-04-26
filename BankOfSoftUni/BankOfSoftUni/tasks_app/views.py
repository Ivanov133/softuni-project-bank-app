
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as views

from BankOfSoftUni.auth_app.models import Profile
from BankOfSoftUni.helpers.common import required_permissions

from BankOfSoftUni.tasks_app.forms import CreateTargetsForm, EditTargetsForm, DeleteTargetsForm
from BankOfSoftUni.tasks_app.models import UserAnnualTargets


@method_decorator(required_permissions(required_permissions=['tasks_app.add_userannualtargets']), name='dispatch')
class CreateTargets(LoginRequiredMixin, views.CreateView):
    form_class = CreateTargetsForm
    template_name = 'main/../../templates/tasks_app/target_create.html'
    success_url = reverse_lazy('index')


@method_decorator(required_permissions(required_permissions=['tasks_app.change_userannualtargets']), name='dispatch')
class EditTargetsView(LoginRequiredMixin, views.UpdateView):
    model = UserAnnualTargets
    form_class = EditTargetsForm
    template_name = 'tasks_app/target_edit.html'
    success_url = reverse_lazy('index')


@method_decorator(required_permissions(required_permissions=['tasks_app.delete_userannualtargets']), name='dispatch')
class DeleteTargetsView(LoginRequiredMixin, views.DeleteView):
    model = UserAnnualTargets
    form_class = DeleteTargetsForm
    template_name = 'tasks_app/target_delete.html'
    success_url = reverse_lazy('index')


def target_menu(request):
    return render(request, 'tasks_app/target_menu.html')


def target_search(request):
    profile = None
    context = {}

    if request.method == 'GET':
        searched_user = request.GET.get('username', None)
        if searched_user:
            profile = Profile.objects.get(user__username=searched_user)
        context['profile'] = profile

    return render(request, 'tasks_app/target_search.html', context)
