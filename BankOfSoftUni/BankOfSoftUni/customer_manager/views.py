from django.http import QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from BankOfSoftUni.customer_manager.forms import CreateCustomerForm, AccountOpenForm, CreateLoanForm
from BankOfSoftUni.customer_manager.models import IndividualCustomer, Account, BankLoan
from BankOfSoftUni.helpers.common import loan_approve, get_next_month_date


class CustomerPanelView(views.DetailView):
    model = IndividualCustomer
    template_name = 'customer_dashboard/customer_details.html'


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

    # get customer and user and assign to account
    if request.method == 'POST':
        form = AccountOpenForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.assigned_user = request.user
            account.customer = customer
            form.save()
            return redirect('customer details', customer.id)
    else:
        form = AccountOpenForm()

    context = {
        'customer': customer,
        'user': request.user,
        'form': form,
        'accounts': accounts,
    }

    return render(request, 'customer_dashboard/customer_details.html', context)


def loan_create(request, pk):
    customer = IndividualCustomer.objects.get(pk=pk)
    # All accounts are used for the form choice field
    accounts = Account.objects.all().filter(customer_id=customer.id)
    context = {
        'customer': customer,
        'accounts': accounts,
    }
    # GET loan principal and duration
    # Pass them on to calculation functions
    # Populate the next form with the returned values
    if request.method == 'GET':
        principal = request.GET.get('principal')
        period = request.GET.get('period')
        if period and principal:
            loan_calculator = loan_approve(customer.annual_income, float(principal), int(period))
            context['loan_result'] = loan_calculator
            context['accounts'] = accounts
            context['principal'] = principal
            context['period'] = period
            form = CreateLoanForm(
                accounts,
                customer,
                request.user,
                loan_calculator['interest_rate'],
                loan_calculator['monthly_payment'],
                principal,
                period,
            )
            context['form'] = form

            # store data in session
            request.session['monthly_payment'] = loan_calculator['monthly_payment']
            request.session['principal'] = principal
            request.session['period'] = period
            request.session['interest_rate'] = loan_calculator['interest_rate']
            request.session.modified = True

    # If loan is confirmed, create loan object with the saved data from the session
    if request.method == 'POST':
        # account = Account.objects.all().filter(pk=request.POST.get('account_credit'))[:1].get()
        account_query = [acc for acc in customer.customer_accounts.all() if
                   acc.account_number == request.POST.get('account_credit')]
        account = list(account_query[:1])[0]
        loan = BankLoan(
            currency="BGN",
            principal=request.session.get('principal'),
            interest_rate=request.session.get('interest_rate'),
            duration_in_years=request.session.get('period'),
            next_monthly_payment_due_date=get_next_month_date(),
            monthly_payment_value=request.session.get('monthly_payment'),
            customer_debtor=context['customer'],
            assigned_user=request.user,
            principal_remainder=request.session.get('principal'),
            account_credit=r,
        )
        loan.save()
        account.available_balance = loan.principal
        account.save()
        return render(request, 'customer_dashboard/customer_details.html', customer.pk)
    return render(request, 'customer_dashboard/loan_create.html', context)
