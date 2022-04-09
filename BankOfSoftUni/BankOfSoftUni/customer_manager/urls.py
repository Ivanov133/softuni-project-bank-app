from django.urls import path

from BankOfSoftUni.customer_manager.views import search_customer_by_parameter, CustomerRegisterView, customer_details

urlpatterns = (
    # path('account/create/', AccountOpenView.as_view(), name='account create'),
    path('details/<int:pk>/', customer_details, name='customer details'),
    path('register/', CustomerRegisterView.as_view(), name='customer register'),
    path('search/', search_customer_by_parameter, name='customer search'),
)
