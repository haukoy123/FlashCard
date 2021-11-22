from django.urls import path
from users import views


app_name = 'users'

urlpatterns = [
    # path('', views.LoginRegisterView, name='LoginRegisterView'),
    path('register/', views.AddUser, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('learn/', views.StacksFcView, name='learn'),
    path('profile/', views.ProfileView, name='profile'),

]
