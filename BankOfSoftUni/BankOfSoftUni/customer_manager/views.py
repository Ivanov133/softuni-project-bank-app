from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from BankOfSoftUni.customer_manager.forms import CreateCustomerForm, AccountOpenForm, CreateLoanForm, LoanEditForm, \
    AccountEditForm, AccountDeleteForm
from BankOfSoftUni.customer_manager.models import IndividualCustomer, Account, BankLoan
from BankOfSoftUni.helpers.common import loan_approve, \
    update_target_list_accounts, set_request_session_loan_params, \
    clear_request_session_loan_params, set_session_error
from BankOfSoftUni.helpers.parametrizations import MAX_LOAN_DURATION_MONTHS_PARAM, MAX_LOAN_PRINCIPAL_PARAM, \
    MIN_LOAN_PRINCIPAL_PARAM, CUSTOMER_MAX_LOAN_EXPOSITION, MIN_LOAN_DURATION_MONTHS_PARAM


# Search customer and redirect to details view
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
                try:
                    customer = IndividualCustomer.objects.get(ucn=searched_value)
                except:
                    pass
            elif form_input_field == 'customer_number':
                customer = [cus for cus in IndividualCustomer.objects.all() if cus.customer_number == searched_value]
            elif form_input_field == 'full_name':
                customer = [cus for cus in IndividualCustomer.objects.all() if cus.full_name == searched_value]

        if customer:
            context = {
                'customer': customer[0]
            }
        else:
            if search_by == None:
                context = {
                    'initial_page_load': True
                }
            else:
                context = {
                    'initial_page_load': False,
                    'customer': f'Could not find customer with {search_by}: {searched_value}!'
                }

        return render(request, 'customer_dashboard/customer_search.html', context)


@login_required()
def customer_details(request, pk):
    customer = IndividualCustomer.objects.get(pk=pk)
    customer.bankloan_set.all()
    accounts = customer.customer_accounts.all()
    # loans = BankLoan.objects.all().filter(customer_debtor_id=pk)
    loans = customer.bankloan_set.all()

    # get customer and user and assign to account
    if request.method == 'POST':
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


class CustomerRegisterView(LoginRequiredMixin, views.CreateView):
    form_class = CreateCustomerForm
    template_name = 'customer_dashboard/customer_register.html'
    success_url = reverse_lazy('customer details')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # redirect to details page by getting pk from url
    def form_valid(self, form):
        customer = form.save()
        self.pk = customer.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('customer details', kwargs={'pk': self.pk})


class CustomerEditView(LoginRequiredMixin, views.UpdateView):
    model = IndividualCustomer
    template_name = 'customer_dashboard/customer_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('customer details')

    def get_success_url(self):
        return reverse_lazy('customer details', kwargs={'pk': self.object.id})


class CustomerDeleteView(LoginRequiredMixin, views.DeleteView):
    model = IndividualCustomer
    success_url = reverse_lazy('index')


class AccountUpdateView(LoginRequiredMixin, views.UpdateView):
    model = Account
    template_name = 'customer_dashboard/account_edit.html'
    form_class = AccountEditForm
    success_url = reverse_lazy('customer details')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['accounts'] = Account.objects.all().filter(customer_id=self.object.pk)
        return kwargs

    def get_success_url(self):
        return reverse_lazy('customer details', kwargs={'pk': self.kwargs['pk']})


class AccountDeleteView(LoginRequiredMixin, views.DeleteView):
    model = Account
    success_url = reverse_lazy('customer details')
    form_class = AccountDeleteForm
    template_name = 'customer_dashboard/account_delete.html'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['accounts'] = Account.objects.all().filter(customer_id=self.object.pk)
        return kwargs

    def get_success_url(self):
        return reverse_lazy('customer details', kwargs={'pk': self.kwargs['pk']})


class LoanUpdateView(LoginRequiredMixin, views.UpdateView):
    model = BankLoan
    template_name = 'customer_dashboard/loan_edit.html'
    form_class = LoanEditForm
    success_url = reverse_lazy('customer details')

    # Display all loans info so that user knows how much principal is remaining
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loans'] = BankLoan.objects.all().filter(customer_debtor=self.object.pk)
        context['accounts'] = Account.objects.all().filter(customer_id=self.object.pk)

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['accounts'] = Account.objects.all().filter(customer_id=self.object.pk)
        kwargs['loans'] = BankLoan.objects.all().filter(customer_debtor=self.object.pk)
        return kwargs

    def get_success_url(self):
        return reverse_lazy('customer details', kwargs={'pk': self.kwargs['pk']})


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
                                f' months. Principal must be in range {MIN_LOAN_PRINCIPAL_PARAM} - {MAX_LOAN_PRINCIPAL_PARAM} BGN!'
                set_session_error(request, error_message)
                return redirect('loan check', customer.pk)

            if customer_loan_exposition + float(principal) > CUSTOMER_MAX_LOAN_EXPOSITION:
                error_message = f'Current loan exposition for this customer exceeded by ' \
                                f'{customer_loan_exposition + float(principal) - CUSTOMER_MAX_LOAN_EXPOSITION:.2f} BGN'
                set_session_error(request, error_message)

                return redirect('loan check', customer.pk)

            loan_calculator = loan_approve(customer.annual_income, float(principal), int(period))
            context['loan_data'] = loan_calculator
            set_request_session_loan_params(request, loan_calculator, principal, period, customer.id)
            if request.session.get('error', None):
                del request.session['error']

    return render(request, 'customer_dashboard/loan_check.html', context)
