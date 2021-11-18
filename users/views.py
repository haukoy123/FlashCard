from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import generic
from users.models import User
from users.forms import UserForm, LoginForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.urls.base import reverse_lazy  # REVIEW: import thừa



# REVIEW: def login
def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        error = list()  # REVIEW: biến ko dùng

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('oke')
            else:
                form.add_error('__all__', 'tai khoan hoac mat khau khong chinh xac')  # REVIEW: sửa tiếng Việt có dấu
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})



def AddUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(True)  # REVIEW: save(commit=True), không cần thiết?
            return HttpResponseRedirect(reverse('users:login'))  # REVIEW: dùng hàm redirect
    else:
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
