from django.urls import path
from . import views
appname='signin'

urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.loginview, name='loginview'),
    path('signin/', views.signinview, name='signinview'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('otp/', views.otp, name='otp'),
    path('save/', views.save, name='save'),
    path('history/', views.history, name='history'),
    path('upload/', views.uploadfile, name='upload'),
    path('result/', views.output, name='output'),
    path('logout/', views.logoutview, name='logout')
    ]


    