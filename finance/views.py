from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .forms import RegisterForm

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home_authenticated.html')  # Для аутентифицированных пользователей
    return render(request, 'home.html')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Тут можно заменить на RegisterForm, если она нужна
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация успешна! Вы вошли в систему.")
            return redirect('home')
        else:
            messages.error(request, "Ошибка при регистрации. Проверьте данные.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)  
            if user:
                login(request, user)
                return redirect('home')  
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            messages.error(request, "Ошибка валидации формы.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')


