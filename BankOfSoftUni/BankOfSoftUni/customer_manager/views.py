from django.http import QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from BankOfSoftUni.customer_manager.forms import CreateCustomerForm, AccountOpenForm, EditCustomerForm
from BankOfSoftUni.customer_manager.models import Customer


class CustomerPanelView(views.DetailView):
    model = Customer
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
    model = Customer
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
                    customer = Customer.objects.get(ucn=searched_value)
                except:
                    pass
            elif form_input_field == 'customer_number':
                customer = [cus for cus in Customer.objects.all() if cus.customer_number == searched_value]
            elif form_input_field == 'full_name':
                customer = [cus for cus in Customer.objects.all() if cus.full_name == searched_value]

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


# class AccountOpenView(views.CreateView):
#     form_class = AccountOpenForm
#     template_name = 'customer_dashboard/account_create.html'
#     success_url = reverse_lazy('customer details')
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         # kwargs['customer'] = Customer.objects.get(pk=self.kwargs['pk'])
#         # print(kwargs['customer'])
#         return kwargs
#
#     # redirect to details page by getting pk from url
#     def form_valid(self, form):
#         account = form.save()
#         self.pk = account.pk
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse('customer details', kwargs={'pk': self.pk})
#

def customer_details(request, pk):
    customer = Customer.objects.get(pk=pk)
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
