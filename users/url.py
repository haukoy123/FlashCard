from django.urls import path
from users import views


app_name = 'users'

urlpatterns = [
    path('register/', views.AddUser, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
]
