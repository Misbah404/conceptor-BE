from django.urls import path
from api.views import *

urlpatterns = [
    path('register', Register.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('change-password', ChangePassword.as_view(), name='change-password'),
    path('forgot-password', ForgotPassword.as_view(), name='forgot-password'),
    path('reset-password/<uidb64>/<token>', ResetPassword.as_view(), name='reset-password'),
    path('logout', Logout.as_view(), name='logout'),
    path('email', SendEmail.as_view(), name='email'),
    path('question', QuestionView.as_view(), name='question'),
    path('user', UserView.as_view(), name='user'),
    path('user-company', UserCompanyView.as_view(), name='user-company'),
    path('user-company/<id>', UserCompanyDetailView.as_view(), name='user-company-detail'),
    path('user-lead', UserLeadView.as_view(), name='user-lead'),
    path('user-lead/<id>', UserLeadDetailView.as_view(), name='user-lead-detail'),
    path('communication', CommunicationView.as_view(), name='communication'),
    path('programx', ProgramX.as_view(), name='programx'),
]