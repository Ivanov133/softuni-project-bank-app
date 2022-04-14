from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib.auth import mixins as auth_mixin

from BankOfSoftUni.auth_app.forms import CreateProfileForm
from BankOfSoftUni.auth_app.models import Profile


class ProfileEditView(views.UpdateView):
    model = Profile
    template_name = 'users/profile_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('upload target')

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.pk})


class UserRegisterView(views.CreateView):
    form_class = CreateProfileForm
    template_name = 'users/create_user.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().success_url()


class UserLoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class HomeView(views.TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        return {
            'test': 'IT WORRKS'
        }


def logout_view(request):
    logout(request)
    return redirect('index')


class ProfileDetailsView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = Profile
    template_name = 'users/profile_details.html'

