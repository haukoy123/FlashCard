import re

from django.shortcuts import redirect, render
from django.views import generic, View
from django.contrib.auth import get_user_model
from users.forms import UserForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


def LoginView(request):
    # print(request.user.is_authenticated)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        regex = re.compile(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$")

        if regex.match(request.POST['username']):
            try:
                username = get_user_model().objects.get(email=request.POST['username']).username
                form = LoginForm({'username':username, 'password': request.POST['password']})
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
            return redirect('users:login')
    else:
        form = UserForm()
    return LoginRegisterForm(request, register_form=form)


def LoginRegisterForm(request, register_form = UserForm(), login_form = LoginForm()):
    return render(request,'users/login_register.html', {
            'register_form': register_form,
            'login_form': login_form
        }
    )



def StacksFcView(request):
    if request.user.is_authenticated:
        return render(request,'users/stacks_flash_cards.html')
    else:
        return redirect('users:login')


def ProfileView(request):
    pass

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