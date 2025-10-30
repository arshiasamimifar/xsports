from django.urls import path
from .views import LoginView, RegisterView, ActivateAccountView, ForgotPasswordView, ResetPasswordView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate-account/<str:email_active_code>/', ActivateAccountView.as_view(), name='activate'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<str:email_active_code>/', ResetPasswordView.as_view(), name='reset_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
]