from django.urls import path
from users import views, forms
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'users'

urlpatterns = [
    path('register/', views.AddUser, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('profile/', views.ProfileView, name='profile'),
    path('password-change/', views.PasswordChange, name='password-change'),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset_form.html',
            success_url = reverse_lazy('users:password_reset_done'),
            email_template_name='users/password_reset_email.txt',
            html_email_template_name='users/password_reset_email.html'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            form_class = forms.SetPasswordFormCustom,
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
