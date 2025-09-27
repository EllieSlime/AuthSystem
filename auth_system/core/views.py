from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User

def home(request):
    return render(request, "core/home.html")
def about(request):
    return render(request, "core/about.html")
def account(request):
    return render(request, "core/account.html")
def adminn(request):
    return render(request, "core/adminn.html")
def assistant(request):
    return render(request, "core/assistant.html")
def device(request):
    return render(request, "core/device.html")
def error401(request):
    return render(request, "core/error401.html")
def error403(request):
    return render(request, "core/error403.html")
def login_page(request):
    return render(request, "core/login_page.html")
def settings(request):
    return render(request, "core/settings.html")
def lobby(request):
    return render(request, "core/lobby.html")
def lobby_add(request):
    return render(request, "core/lobby_add.html")
def lobby_set(request):
    return render(request, "core/lobby_set.html")
def lobby_cre(request):
    return render(request, "core/lobby_cre.html")

def register_view(request):
    #print("=== register_view вызван. method:", request.method)

    if request.method == "POST":
        form = RegisterForm(request.POST)
        #print("POST данные (регистрация):", request.POST)

        if form.is_valid():
            #print("RegisterForm валиден")
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            #print("Новый пользователь сохранён:", user.username, user.email)

            login(request, user)  # сразу авторизуем
            #print("Пользователь авторизован после регистрации:", user.username)

            messages.success(request, "Регистрация завершена! Выполняется вход...")
            return redirect("lobby")
        else:
            #print("RegisterForm НЕ валиден. Ошибки:", form.errors)
            return render(request, "core/login_page.html", {
                'active_tab': 'register',
                "register_form": form,
                "login_form": LoginForm()
            })
    else:
        #print("Регистрация: GET-запрос")
        form = RegisterForm()

    return render(request, "core/login_page.html", {
        "register_form": form,
        "login_form": LoginForm()
    })


def login_view(request):
    #print("=== login_view вызван. method:", request.method)

    if request.method == "POST":
        #print("POST данные (логин):", request.POST)
        form = LoginForm(request.POST)

        if form.is_valid():
            #print("LoginForm валиден")
            user = form.cleaned_data.get("user")
            #print("cleaned_data.user =", user)

            if user:
                login(request, user)
                #print("Успешный вход:", user.username)
                messages.success(request, "Добро пожаловать, вы вошли!")
                return redirect("lobby")
            #else:
                #print("⚠️ user = None, хотя форма валидна")
        #else:
            #print("LoginForm НЕ валиден. Ошибки:", form.errors)

        messages.error(request, "Неверный логин или пароль.")
    else:
        #print("Логин: GET-запрос")
        form = LoginForm()

    return render(request, "core/login_page.html", {
        "login_form": form,
        "register_form": RegisterForm()
    })


def logout_view(request):
    #print("=== logout_view вызван. method:", request.method)
    logout(request)
    #print("Пользователь разлогинен")
    return redirect("home")