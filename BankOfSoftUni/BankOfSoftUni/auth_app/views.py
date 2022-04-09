from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth import logout

from BankOfSoftUni.auth_app.forms import CreateProfileForm


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
