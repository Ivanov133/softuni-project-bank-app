from django.urls import path

from BankOfSoftUni.auth_app.views import UserRegisterView, HomeView, UserLoginView, logout_view, ProfileDetailsView, \
    ProfileEditView

urlpatterns = (
    path('', HomeView.as_view(), name='index'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile edit'),
)
