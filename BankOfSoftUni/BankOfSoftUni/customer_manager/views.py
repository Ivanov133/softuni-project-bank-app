from django.http import QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixin
from BankOfSoftUni.auth_app.models import Profile
from BankOfSoftUni.customer_manager.forms import CreateCustomerForm, AccountOpenForm, EditCustomerForm
from BankOfSoftUni.customer_manager.models import Customer


class CustomerPanelView(views.DetailView):
    model = Customer
    # form_class = AccountOpenForm
    template_name = 'customer_dashboard/customer_details.html'
    # success_url = reverse_lazy('index')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['customer'] = {
    #         self.
    #     }
    #     return {
    #         'context': context
    #     }

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     kwargs['customer'] = Customer.objects.get(pk=self.kwargs['pk'])
    #     print(type(self.kwargs['pk']))
    #     return kwargs


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


class CustomerEditView(views.CreateView):
    form_class = EditCustomerForm
    template_name = 'customer_dashboard/customer_edit.html'
    success_url = reverse_lazy('customer details')


class ProfileDetailsView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = Profile
    template_name = 'users/profile_details.html'
    context_object_name = 'p_details'


def search_customer_by_parameter(request):
    customer = None
    search_by = None

    # Depending on what the search parameter is, different query is sent / or filter is made
    if request.method == 'GET':
        searched_value = request.GET.get('parameter')
        for form_input_field in QueryDict.dict(request.GET):
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
                'customer': customer
            }
        else:
            context = {
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
