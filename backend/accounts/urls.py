from django.urls import path
from .views import HomePageView, UserSignup, Logout, Login, SendOtp, Check, Password_reset

app_name = 'accounts'

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('signup/', UserSignup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('send_otp/', SendOtp.as_view(), name='send_otp'),
    path('otp_check/', Check.as_view(), name='otp_check'),
    path('change_password/', Password_reset.as_view(), name='change_password'),
]