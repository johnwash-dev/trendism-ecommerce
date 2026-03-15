from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('', views.email_login, name='login'),
    path('verify_otp/', views.verify_otp, name= 'verify_otp'),
    path("resend-otp/", views.resend_otp, name="resend_otp"),
    path('become_seller/', views.become_seller, name = 'become_seller'),
    path('seller_submitted/', views.seller_submitted, name = 'seller_submitted'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
