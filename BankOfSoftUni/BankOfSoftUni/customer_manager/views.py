from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from BankOfSoftUni.customer_manager.forms import CreateCustomerForm, AccountOpenForm, CreateLoanForm
from BankOfSoftUni.customer_manager.models import IndividualCustomer, Account, BankLoan
from BankOfSoftUni.helpers.common import loan_approve, get_next_month_date, \
    update_target_list_accounts, update_target_list_loans, set_request_session_loan_params, \
    clear_request_session_loan_params
from BankOfSoftUni.helpers.parametrizations import ALLOWED_CURRENCIES, MAX_LOAN_DURATION_YEARS, MAX_LOAN_PRINCIPAL, \
    MIN_LOAN_PRINCIPAL, CUSTOMER_MAX_LOAN_EXPOSITION


class CustomerPanelView(views.DetailView):
    model = IndividualCustomer
    template_name = 'customer_dashboard/customer_details.html'


class LoanCreateView(views.CreateView):
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
        return reverse_lazy('customer details', kwargs={'pk': self.request.session.get('customer_id')})


class CustomerRegisterView(views.CreateView):
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


class CustomerEditView(views.UpdateView):
    model = IndividualCustomer
    template_name = 'customer_dashboard/customer_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('customer details')

    def get_success_url(self):
        return reverse_lazy('customer details', kwargs={'pk': self.object.id})


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


def customer_details(request, pk):
    customer = IndividualCustomer.objects.get(pk=pk)
    accounts = customer.customer_accounts.all()
    loans = BankLoan.objects.all().filter(customer_debtor_id=pk)

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
    # GET loan principal and duration
    # Pass them on to calculation functions
    if request.method == 'GET':
        principal = request.GET.get('principal')
        period = request.GET.get('period')
        if period and principal:
            if MIN_LOAN_PRINCIPAL > float(principal) or float(
                    principal) > MAX_LOAN_PRINCIPAL or MAX_LOAN_DURATION_YEARS < int(period) or int(period) < 1:
                request.session[
                    'error'] = f'Please enter valid parameters! Maximum period is {MAX_LOAN_DURATION_YEARS} years. Principal must be in range {MIN_LOAN_PRINCIPAL} - {MAX_LOAN_PRINCIPAL} BGN!'
                return redirect('loan check', customer.pk)

            if customer_loan_exposition + float(principal) > CUSTOMER_MAX_LOAN_EXPOSITION:
                request.session[
                    'error'] = f'Current loan exposition for this customer exceeded by {customer_loan_exposition + float(principal) - CUSTOMER_MAX_LOAN_EXPOSITION:.2f} BGN'
                return redirect('loan check', customer.pk)

            # store data in session to pass along for create loan view

            loan_calculator = loan_approve(customer.annual_income, float(principal), int(period))
            context['loan_data'] = loan_calculator
            set_request_session_loan_params(request, loan_calculator, principal, period, customer.id)

    return render(request, 'customer_dashboard/loan_check.html', context)
