from django.shortcuts import redirect, render
from django.views import generic
from users.models import User
from users.forms import UserForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


def LoginView(request):
    print(request.user.is_authenticated)
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('oke')
            else:
                form.add_error('__all__', 'Tài khoản hoặc mật khẩu không chính xác!')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})



def LogoutView(request):
    logout(request)
    return render(request, 'users/login.html', {'form': LoginForm()})


def AddUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:login')

        form = UserForm()
    return render(request, 'users/add_user.html', {'form': form})




# class AddUser(generic.CreateView):
#     model = User
#     fields = '__all__'
#     # form_class = UserForm
#     template_name = 'users/add_user.html'
#     # success_url = reverse_lazy('users:login')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
