from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileUpdateForm, CurrentPasswordForm, PasswordChangeCustomForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import (
    ProfileUpdateForm,
    PasswordChangeCustomForm,
    ProfileUpdateForm,
    CurrentPasswordForm,
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
    # инициализация форм (не привязанные)
    profile_form = ProfileUpdateForm(instance=request.user)
    current_password_form = CurrentPasswordForm(user=request.user)
    password_form = PasswordChangeCustomForm(user=request.user)

    active_tab = "profile"           # по умолчанию
    show_new_password_form = False   # показывать второй шаг смены пароля?

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        # ------------- профиль -------------
        if form_type == "profile":
            profile_form = ProfileUpdateForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Данные профиля обновлены.")
                return redirect("settings")  # успешное сохранение — редирект
            else:
                messages.error(request, "Ошибка при обновлении профиля.")
            active_tab = "profile"

        # ------------- шаг 1: проверка текущего пароля -------------
        elif form_type == "password_verify":
            # привязываем форму проверки текущего пароля
            current_password_form = CurrentPasswordForm(request.user, request.POST)
            if current_password_form.is_valid():
                # пароль верный — показываем форму ввода нового пароля
                show_new_password_form = True
                active_tab = "password"
                # password_form остаётся unbound (пустой) — пользователь введёт новый пароль
                # рендерим страницу (не редирект), чтобы остались ошибки/контекст
                return render(request, "core/settings_page.html", {
                    "profile_form": profile_form,
                    "current_password_form": current_password_form,
                    "password_form": password_form,
                    "active_tab": active_tab,
                    "show_new_password_form": show_new_password_form,
                })
            else:
                # ошибка проверки текущего пароля — current_password_form содержит ошибки
                messages.error(request, "Неверный текущий пароль.")
                active_tab = "password"

        # ------------- шаг 2: установка нового пароля -------------
        elif form_type == "password_change":
            password_form = PasswordChangeCustomForm(request.user, request.POST)
            if password_form.is_valid():
                new_password = password_form.cleaned_data["new_password"]
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Пароль успешно изменён.")
                return redirect("settings")
            else:
                # показать ошибки на шаге ввода нового пароля
                messages.error(request, "Ошибка при смене пароля.")
                active_tab = "password"
                show_new_password_form = True

        else:
            # неизвестный form_type — просто оставим всё как есть
            active_tab = request.POST.get("form_type", "profile")

    # GET или падение валидации — отрисуем текущие формы
    return render(request, "core/settings_page.html", {
        "profile_form": profile_form,
        "current_password_form": current_password_form,
        "password_form": password_form,
        "active_tab": active_tab,
        "show_new_password_form": show_new_password_form,
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


'''@login_required
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
    return redirect("settings")'''


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

@login_required
def deactivate_profile(request):
    """Деактивировать профиль (отключить вход в аккаунт)"""
    user = request.user
    user.is_active = False
    user.save()
    logout(request)
    messages.info(request, "Ваш профиль был деактивирован. Для повторной активации обратитесь к администратору.")
    return redirect("home")