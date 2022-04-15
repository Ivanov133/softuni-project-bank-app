from django.db.models import Model
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib.auth import mixins as auth_mixin

from BankOfSoftUni.auth_app.forms import CreateProfileForm
from BankOfSoftUni.auth_app.models import Profile
from BankOfSoftUni.helpers.parametrizations import ALLOWED_CURRENCIES, \
    LOAN_INTEREST_RATES_BASED_ON_PRINCIPAL_MIN_THRESHOLD_BGN, LOAN_INTEREST_RATES_DEDUCTIONS_BASED_ON_DURATION_YEARS, \
    MAX_LOAN_DURATION_YEARS, MAX_LOAN_PRINCIPAL, MIN_LOAN_PRINCIPAL, CUSTOMER_MAX_LOAN_EXPOSITION
from BankOfSoftUni.tasks_app.models import UserAnnualTargets


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
        bank_target_completion = UserAnnualTargets.objects.all()
        context = {
            "currency_ratios": ALLOWED_CURRENCIES,
            "loans_max_duration": MAX_LOAN_DURATION_YEARS,
            "loans_max_exposition": CUSTOMER_MAX_LOAN_EXPOSITION,
            "loan_max_principal": MAX_LOAN_PRINCIPAL,
            "loan_min_principal": MIN_LOAN_PRINCIPAL,
            "loans_interest_rate": LOAN_INTEREST_RATES_BASED_ON_PRINCIPAL_MIN_THRESHOLD_BGN,
            "loans_interest_rates_deduction": LOAN_INTEREST_RATES_DEDUCTIONS_BASED_ON_DURATION_YEARS,
            "bank_target_completion": bank_target_completion
        }

        return context


def logout_view(request):
    logout(request)
    return redirect('index')


class ProfileDetailsView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = Profile
    template_name = 'users/profile_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.pk
        try:
            profile_target_data = UserAnnualTargets.objects.get(pk=self.object.pk)
        except UserAnnualTargets.DoesNotExist:
            profile_target_data = 'There is no uploaded target for this user.'
        context['profile_target_data'] = profile_target_data

        return context
