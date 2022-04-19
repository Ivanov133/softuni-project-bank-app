from django.urls import path

from BankOfSoftUni.customer_manager.views import search_customer_by_parameter, CustomerRegisterView, customer_details, \
    CustomerEditView, loan_check, LoanCreateView, LoanUpdateView, AccountUpdateView

urlpatterns = (
    path('customer-details/<int:pk>/', customer_details, name='customer details'),
    path('customer-register/', CustomerRegisterView.as_view(), name='customer register'),
    path('customer-edit/<int:pk>/', CustomerEditView.as_view(), name='customer edit'),
    path('customer-search/', search_customer_by_parameter, name='customer search'),
    path('loan-parametrize/<int:pk>/', loan_check, name='loan check'),
    path('loan-create/<int:pk>/', LoanCreateView.as_view(), name='loan create'),
    path('loan-edit/<int:pk>/', LoanUpdateView.as_view(), name='loan edit'),
    path('account-deposit/<int:pk>/', AccountUpdateView.as_view(), name='account edit'),
)
