import re
from django.shortcuts import redirect, render
from django.views import generic, View
from users.forms import UserForm, LoginForm, PasswordChangeForm, ProfileForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email_regex = re.compile(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$")
        if email_regex.match(request.POST['username']):
            try:
                username = get_user_model().objects.get(email=request.POST['username']).username
                form = LoginForm({'username':username, 'password': request.POST['password']})
            except username.DoesNotExist as e:
                form.add_error('__all__', 'Tài khoản hoặc mật khẩu không chính xác!')

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Đăng nhập thành công.')
                return redirect('cardgroups:learn')
            else:
                messages.error(request, 'Đăng nhập thất bại.')
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
                messages.success(request, 'Đăng kí tài khoản thành công.')
            return redirect('cardgroups:learn')
        else:
            messages.error(request, 'Đăng kí tài khoản thất bại.')
    else:
        form = UserForm()
    return LoginRegisterForm(request, register_form=form)


def LoginRegisterForm(request, register_form = UserForm(), login_form = LoginForm()):
    return render(request,'users/login_register.html', {
            'register_form': register_form,
            'login_form': login_form
        }
    )




@login_required()
def ProfileView(request):
    if request.method == 'POST':
        user_form = ProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Cập nhật thông tin cá nhân thành công.')
            return redirect('users:profile')
        else:
            messages.error(request, 'Cập nhật thông tin cá nhân thất bại.')

    else:
        user_form = ProfileForm(instance=request.user)
    return render(request,'users/profile.html',{'form': user_form})


@login_required()
def PasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['current_password']):
                user.set_password(form.cleaned_data['password'])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Thay đổi mật khẩu thành công.')
                return redirect('cardgroups:learn')
            else:
                messages.error(request, 'Thay đổi mật khẩu thất bại.')
                form.add_error('current_password', 'Mật khẩu không đúng')
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
