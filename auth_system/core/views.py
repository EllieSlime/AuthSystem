from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileUpdateForm, AddressUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import (
    ProfileUpdateForm,
    AddressUpdateForm,
    PasswordChangeCustomForm,
)


from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


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
def settings_page(request):
    return render(request, "core/settings_page.html")
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
    if request.user.is_authenticated:
        return redirect("lobby")

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
    if request.user.is_authenticated:
        return redirect("lobby")

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

@login_required
def settings_view(request):
    # для адреса используем initial, так как это не поле User по умолчанию
    address_initial = {"address": getattr(request.user, "address", "")}

    if request.method == "POST":
        form_type = request.POST.get("form_type", "profile")

        if form_type == "profile":
            profile_form = ProfileUpdateForm(request.POST, instance=request.user)
            address_form = AddressUpdateForm(initial=address_initial)
            password_form = PasswordChangeCustomForm(user=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Данные профиля обновлены.")
                return redirect("settings")

        elif form_type == "address":
            profile_form = ProfileUpdateForm(instance=request.user)
            address_form = AddressUpdateForm(request.POST)
            password_form = PasswordChangeCustomForm(user=request.user)
            if address_form.is_valid():
                request.user.address = address_form.cleaned_data.get("address", "")
                request.user.save()
                messages.success(request, "Адрес обновлён.")
                return redirect("settings")

        elif form_type == "password":
            profile_form = ProfileUpdateForm(instance=request.user)
            address_form = AddressUpdateForm(initial=address_initial)
            password_form = PasswordChangeCustomForm(request.user, request.POST)
            if password_form.is_valid():
                request.user.set_password(password_form.cleaned_data["new_password"])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Пароль успешно изменён.")
                return redirect("settings")

        else:
            profile_form = ProfileUpdateForm(request.POST, instance=request.user)
            address_form = AddressUpdateForm(request.POST)
            password_form = PasswordChangeCustomForm(request.user, request.POST)

    else:  # GET-запрос
        profile_form = ProfileUpdateForm(instance=request.user)   # 🔹 без initial
        address_form = AddressUpdateForm(initial=address_initial)
        password_form = PasswordChangeCustomForm(user=request.user)

    return render(request, "core/settings_page.html", {
        "profile_form": profile_form,
        "address_form": address_form,
        "password_form": password_form,
        "active_tab": request.POST.get("form_type", "edit-tab"),
    })

@login_required
def update_profile(request):
    """Обновление ФИО, email, телефона"""
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.full_name = form.cleaned_data["full_name"]
            user.phone = form.cleaned_data.get("phone", "")
            user.save()
            messages.success(request, "Данные профиля обновлены.")
            return redirect("settings")
        else:
            messages.error(request, "Ошибка при обновлении данных.")
    return redirect("settings")


@login_required
def update_address(request):
    """Обновление адреса"""
    if request.method == "POST":
        form = AddressUpdateForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data["address"]
            request.user.address = address
            request.user.save()
            messages.success(request, "Адрес обновлен.")
        else:
            messages.error(request, "Ошибка при обновлении адреса.")
    return redirect("settings")


@login_required
def change_password(request):
    """Смена пароля"""
    if request.method == "POST":
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # остаёмся в сессии
            messages.success(request, "Пароль успешно изменён.")
            return redirect("settings")
        else:
            messages.error(request, "Ошибка при смене пароля.")
    return redirect("settings")