import re
from users.models import User

from django.shortcuts import redirect, render
from django.views import generic, View
from django.contrib.auth import get_user_model
from users.forms import UserForm, LoginForm, PasswordChangeForm, ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import views
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse_lazy

def LoginView(request):
    # print(request.user.is_authenticated)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # REVIEW: đặt tên biến cụ thể hơn. VD: `email_regex`
        regex = re.compile(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$")

        if regex.match(request.POST['username']):
            try:
                username = get_user_model().objects.get(email=request.POST['username']).username
                form = LoginForm({'username':username, 'password': request.POST['password']})
            # REVIEW: cần bắt exception cụ thể, tránh bắt chung chung thế này.
            # except User.DoesNotExist
            except Exception as e:
                form.add_error('__all__', 'Tài khoản hoặc mật khẩu không chính xác!')

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:learn')
            else:
                form.add_error('__all__', 'Tài khoản hoặc mật khẩu không chính xác!')
    else:
        form = LoginForm()

    return LoginRegisterForm(request=request, login_form=form)




def LogoutView(request):
    logout(request)
    return redirect('users:login')



def AddUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('users:learn')
    else:
        form = UserForm()
    return LoginRegisterForm(request, register_form=form)


def LoginRegisterForm(request, register_form = UserForm(), login_form = LoginForm()):
    return render(request,'users/login_register.html', {
            'register_form': register_form,
            'login_form': login_form
        }
    )



@login_required(login_url='users:login')
def StacksFcView(request):
    return render(request,'users/stacks_flash_cards.html')



@login_required(login_url='users:login')  # REVIEW: `login_url` có thể config ở settings.py
def ProfileView(request):
    # REVIEW: nên thêm thông báo cho người dùng khi thành công/thất bại.
    # Django có hỗ trợ thông báo qua module django.contrib.messages -> tìm hiểu
    if request.method == 'POST':
        user_form = ProfileForm(instance=request.user, data=request.POST, files=request.FILE)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = ProfileForm(instance=request.user)
    return render(request,'users/profile.html',{'form': user_form})


@login_required(login_url='users:login')
def PasswordChange(request):
    if request.method == 'POST':
        # REVIEW: nên refactor logic đổi mật khẩu ra view
        form = PasswordChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.instance)
            return redirect('users:learn')
    else:
        form = PasswordChangeForm()
    return render(request, 'users/password_change.html', {'form': form})



# class AddUser(View):
#     # model = User
#     # fields = '__all__'
#     # # form_class = UserForm
#     template_name = 'users/add_user.html'
#     # # success_url = reverse_lazy('users:login')

#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     return context

#     def get(self, request, *args, **kwargs):
#         form = UserForm()
#         return render(request, self.template_name, {'form': form})
