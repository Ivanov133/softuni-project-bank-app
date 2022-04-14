from django.urls import path

from BankOfSoftUni.tasks_app.views import CreateTargets

urlpatterns = (
    path('upload/', CreateTargets.as_view(), name='upload target'),
)