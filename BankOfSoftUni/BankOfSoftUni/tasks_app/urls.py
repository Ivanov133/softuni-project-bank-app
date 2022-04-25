from django.urls import path

from BankOfSoftUni.tasks_app.views import CreateTargets, EditTargetsView, DeleteTargetsView, target_menu, target_search

urlpatterns = (
    path('', target_menu, name='target menu'),
    path('search/', target_search, name='search target'),
    path('upload/', CreateTargets.as_view(), name='upload target'),
    path('edit/<int:pk>/', EditTargetsView.as_view(), name='edit target'),
    path('delete/<int:pk>/', DeleteTargetsView.as_view(), name='delete target'),
)