from django.urls import path

from BankOfSoftUni.customer_manager.views import search_customer_by_parameter, CustomerRegisterView, customer_details, \
    CustomerEditView, loan_create

urlpatterns = (
    path('details/<int:pk>/', customer_details, name='customer details'),
    path('register/', CustomerRegisterView.as_view(), name='customer register'),
    path('edit/<int:pk>/', CustomerEditView.as_view(), name='customer edit'),
    path('search/', search_customer_by_parameter, name='customer search'),
    path('details/loan/<int:pk>/', loan_create, name='loan create'),
)
