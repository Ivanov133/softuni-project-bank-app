from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic as views

from BankOfSoftUni.auth_app.models import Profile
from BankOfSoftUni.auth_app.views import internal_error
from BankOfSoftUni.customer_manager.forms import CreateCustomerForm, AccountOpenForm, CreateLoanForm, LoanEditForm, \
    AccountEditForm, AccountDeleteForm, LoanDeleteForm, CustomerDeleteForm
from BankOfSoftUni.customer_manager.models import IndividualCustomer, Account, BankLoan
from BankOfSoftUni.helpers.common import loan_approve, \
    update_target_list_accounts, set_request_session_loan_params, \
    clear_request_session_loan_params, set_session_error, required_permissions
from BankOfSoftUni.helpers.parametrizations import MAX_LOAN_DURATION_MONTHS_PARAM, MAX_LOAN_PRINCIPAL_PARAM, \
    MIN_LOAN_PRINCIPAL_PARAM, CUSTOMER_MAX_LOAN_EXPOSITION, MIN_LOAN_DURATION_MONTHS_PARAM, ALLOWED_CURRENCIES


# Search customer by given attribute and redirect details/edit view
@login_required()
def search_customer_by_parameter(request):
    customer = None
    search_by = None
    searched_value = None

    # Depending on what the search parameter is, different query is sent / or filter is made
    if request.method == 'GET':
        for form_input_field in QueryDict.dict(request.GET):
            searched_value = request.GET.get(f'{form_input_field}')
            search_by = form_input_field
            if form_input_field == 'ucn':
                customer = IndividualCustomer.objects.get(ucn=searched_value)
            elif form_input_field == 'document_number':
                customer = IndividualCustomer.objects.get(document_number=searched_value)
            elif form_input_field == 'full_name':
                customer = [cus for cus in IndividualCustomer.objects.all() if cus.full_name == searched_value]
                customer = customer[0]

        if customer:
            context = {
                'customer': customer
            }
        else:
            if not search_by:
                context = {
                    'initial_page_load': True
                }
            else:
                context = {
                    'initial_page_load': False,
                    'customer': f'Could not find customer with {search_by}: {searched_value}!'
                }

        return render(request, 'customer_dashboard/customer_search.html', context)


# Contains customer data and links to loan/account CRUD
@login_required()
def customer_details(request, pk):
    customer = IndividualCustomer.objects.get(pk=pk)
    customer.bankloan_set.all()
    accounts = customer.customer_accounts.all()
    loans = customer.bankloan_set.all()

    # If POST request is made, create Account Object
    # Add permission check manually, since the details view is accessible to all, but account creation is not
    if request.method == 'POST':
        profile = None
        try:
            profile = Profile.objects.get(pk=request.user.id)
        except Profile.DoesNotExist:
            pass
        context = {}
        if not request.user.has_perm(['customer_manager.add_account']):
            context[
                'error'] = f'Access denied. User {request.user.username} has no permission to ' \
                           f'access/alter this data. Currently the user has access rights based on ' \
                           f'his/her role - "{profile.employee_role}". Please contact administrator ' \
                           f'if access needs to be given.'
            return internal_error(request, context)
        form = AccountOpenForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.assigned_user = request.user
            account.customer = customer
            update_target_list_accounts(request.user.id)
            form.save()
            return redirect('customer details', customer.id)
    else:
        form = AccountOpenForm()

    context = {
        'customer': customer,
        'user': request.user,
        'form': form,
        'accounts': accounts,
        'loans': loans,
    }

    return render(request, 'customer_dashboard/customer_details.html', context)


@method_decorator(required_permissions(required_permissions=['customer_manager.view_individualcustomer']),
                  name='dispatch')
class CustomerRegisterView(LoginRequiredMixin, views.CreateView):
    form_class = CreateCustomerForm
    template_name = 'customer_dashboard/customer_register.html'
    success_url = reverse_lazy('customer details')
    model = IndividualCustomer

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('customer details', kwargs={'pk': self.object.pk})


@method_decorator(required_permissions(required_permissions=['customer_manager.change_individualcustomer']),
                  name='dispatch')
class CustomerEditView(LoginRequiredMixin, views.UpdateView):
    model = IndividualCustomer
    template_name = 'customer_dashboard/customer_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('customer details')

    def get_success_url(self):
        return reverse_lazy('customer details', kwargs={'pk': self.object.id})


@method_decorator(required_permissions(required_permissions=['customer_manager.delete_individualcustomer']),
                  name='dispatch')
class CustomerDeleteView(LoginRequiredMixin, views.DeleteView):
    model = IndividualCustomer
    success_url = reverse_lazy('index')
    template_name = 'customer_dashboard/customer_delete.html'
    form_class = CustomerDeleteForm


@method_decorator(required_permissions(required_permissions=['customer_manager.change_account']), name='dispatch')
class AccountUpdateView(LoginRequiredMixin, views.UpdateView):
    model = Account
    template_name = 'customer_dashboard/account_edit.html'
    form_class = AccountEditForm
    success_url = reverse_lazy('customer details')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['account'] = Account.objects.get(pk=self.object.pk)
        return kwargs

    def get_success_url(self):
        pk = Account.objects.get(pk=self.kwargs['pk']).customer_id
        return reverse_lazy('customer details', kwargs={'pk': pk})


@method_decorator(required_permissions(required_permissions=['customer_manager.delete_bankloan']), name='dispatch')
class LoanDeleteView(LoginRequiredMixin, views.DeleteView):
    model = BankLoan
    form_class = LoanDeleteForm
    template_name = 'customer_dashboard/loan-delete.html'
    success_url = reverse_lazy('customer details')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs['debit_account'] = Account.objects.get(pk=self.object.pk)
        kwargs['accounts'] = Account.objects.filter(customer_id=self.object.customer_debtor_id)
        kwargs['loan'] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['accounts'] = Account.objects.filter(customer_id=self.object.customer_debtor_id)

        return context

    def get_success_url(self):
        pk = BankLoan.objects.get(pk=self.kwargs['pk']).customer_debtor_id
        return reverse_lazy('customer details', kwargs={'pk': pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            if not request.POST.get('all_accounts') == 'Cash withdrawal':
                debit_account = Account.objects.get(pk=self.request.POST.get('accounts'))
                if debit_account.currency == 'BGN':
                    debit_account.available_balance -= float(self.object.principal_remainder)
                else:
                    debit_account.available_balance = (debit_account.local_currency - float(
                        self.object.principal_remainder)) / ALLOWED_CURRENCIES[f'{debit_account.currency}']
                debit_account.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(required_permissions(required_permissions=['customer_manager.delete_account']), name='dispatch')
class AccountDeleteView(LoginRequiredMixin, views.DeleteView):
    model = Account
    success_url = reverse_lazy('customer details')
    form_class = AccountDeleteForm
    template_name = 'customer_dashboard/account_delete.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['debit_account'] = Account.objects.get(pk=self.object.pk)
        kwargs['all_accounts'] = Account.objects.filter(customer_id=self.object.customer_id)
        return kwargs

    def get_success_url(self):
        pk = Account.objects.get(pk=self.kwargs['pk']).customer_id
        return reverse_lazy('customer details', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['accounts'] = Account.objects.filter(customer_id=self.object.customer_id)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            debit_account = Account.objects.get(pk=self.kwargs['pk'])
            debit_account_balance_in_bgn = debit_account.available_balance * ALLOWED_CURRENCIES[
                f'{debit_account.currency}']
            if not request.POST.get('all_accounts') == 'Cash withdrawal':
                credit_account = Account.objects.get(pk=request.POST.get('all_accounts'))
                if credit_account.currency == 'BGN':
                    credit_account.available_balance += debit_account_balance_in_bgn
                else:
                    credit_account.available_balance += debit_account_balance_in_bgn / ALLOWED_CURRENCIES[
                        f'{credit_account.currency}']
                credit_account.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(required_permissions(required_permissions=['customer_manager.change_bankloan']), name='dispatch')
class LoanUpdateView(LoginRequiredMixin, views.UpdateView):
    model = BankLoan
    template_name = 'customer_dashboard/loan_edit.html'
    form_class = LoanEditForm
    success_url = reverse_lazy('customer details')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loan'] = BankLoan.objects.get(pk=self.object.pk)
        context['accounts'] = Account.objects.all().filter(customer_id=context['loan'].customer_debtor_id)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['loan'] = BankLoan.objects.get(pk=self.object.pk)
        kwargs['accounts'] = Account.objects.all().filter(customer_id=kwargs['loan'].customer_debtor_id)
        return kwargs

    def get_success_url(self):
        pk = BankLoan.objects.get(pk=self.kwargs['pk']).customer_debtor.id
        return reverse_lazy('customer details', kwargs={'pk': pk})


@method_decorator(required_permissions(required_permissions=['customer_manager.add_bankloan']), name='dispatch')
class LoanCreateView(LoginRequiredMixin, views.CreateView):
    template_name = 'customer_dashboard/loan_create.html'
    form_class = CreateLoanForm
    success_url = reverse_lazy('customer details')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['principal'] = self.request.session.get('principal')
        kwargs['period'] = self.request.session.get('period')
        kwargs['monthly_payment'] = self.request.session.get('monthly_payment')
        kwargs['interest_rate'] = self.request.session.get('interest_rate')
        kwargs['customer'] = IndividualCustomer.objects.get(pk=self.request.session.get('customer_id'))
        kwargs['accounts'] = Account.objects.all().filter(customer_id=kwargs['customer'].pk)
        return kwargs

    def get_success_url(self):
        return reverse_lazy('customer details', kwargs={'pk': self.request.session['customer_id']})


@login_required()
def loan_check(request, pk):
    clear_request_session_loan_params(request)
    customer = IndividualCustomer.objects.get(pk=pk)
    context = {
        'customer': customer,
    }
    clear_request_session_loan_params(request)
    customer_loan_exposition = 0
    for loan in BankLoan.objects.all().filter(customer_debtor=customer.id):
        customer_loan_exposition += loan.principal

    # GET loan principal and duration - check values with parametrization table
    # Check if customer can apply for the loan - if he has an account, if his exposition meets requirements
    # Pass them on to calculation functions to get the needed variables for creating the loan
    # SET session data to pass along to the create view

    if request.method == 'GET':
        principal = request.GET.get('principal')
        period = request.GET.get('period')
        if period and principal:
            if MIN_LOAN_PRINCIPAL_PARAM > float(principal) or float(
                    principal) > MAX_LOAN_PRINCIPAL_PARAM or MAX_LOAN_DURATION_MONTHS_PARAM < int(period) or int(
                period) < MIN_LOAN_DURATION_MONTHS_PARAM:
                error_message = f'Please enter valid parameters! Maximum period is {MAX_LOAN_DURATION_MONTHS_PARAM}' \
                                f' months. Principal must be in range {MIN_LOAN_PRINCIPAL_PARAM} - ' \
                                f'{MAX_LOAN_PRINCIPAL_PARAM} BGN!'
                set_session_error(request, error_message)

                return redirect('loan check', customer.pk)

            if customer_loan_exposition + float(principal) > CUSTOMER_MAX_LOAN_EXPOSITION:
                error_message = f'Current loan exposition for this customer exceeded by ' \
                                f'{customer_loan_exposition + float(principal) - CUSTOMER_MAX_LOAN_EXPOSITION:.2f} BGN'
                set_session_error(request, error_message)

                return redirect('loan check', customer.pk)
            if len(customer.customer_accounts.values_list()) == 0:
                error_message = f'Customer {customer.full_name} must have an open account in order to receive loan!'
                set_session_error(request, error_message)

                return redirect('loan check', customer.pk)

            loan_calculator = loan_approve(customer.annual_income, float(principal), int(period))
            context['loan_data'] = loan_calculator
            set_request_session_loan_params(request, loan_calculator, principal, period, customer.id)
            if request.session.get('error', None):
                del request.session['error']

    return render(request, 'customer_dashboard/loan_check.html', context)
