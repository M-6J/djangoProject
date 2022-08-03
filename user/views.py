from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from user.forms import UserForm

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'user/signup.html', {'form': form})

def profile(request):
    form = UserForm()
    return render(request, 'user/profile.html',{'form': form})

def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
    logout(request)
    return redirect('/')

def modify(request):
    user = request.user
    context = {'user': user}
    return render(request, 'user/modify.html', {'context': context})
