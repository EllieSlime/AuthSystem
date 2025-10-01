from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm, AddDeviceForm, PasswordChangeCustomForm, ProfileUpdateForm, CurrentPasswordForm
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Lobby, LobbyMembership, Device
from .forms import LobbyCreateForm, AddMemberForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


def home(request):
    return render(request, "core/home.html")
def about(request):
    return render(request, "core/about.html")
def adminn(request):
    return render(request, "core/adminn.html")
def assistant(request):
    return render(request, "core/assistant.html")
def error401(request):
    return render(request, "core/error401.html")
def error403(request):
    return render(request, "core/error403.html")
def login_page(request):
    return render(request, "core/login_page.html")
def lobby_add(request):
    return render(request, "core/lobby_add.html")
def lobby_cre(request):
    return render(request, "core/lobby_cre.html")

def register_view(request):
    if request.user.is_authenticated:
        return redirect("lobby")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data["email"]
            user.first_name = form.cleaned_data["full_name"]

            user.set_password(form.cleaned_data["password"])
            user.save()

            login(request, user)

            messages.success(request, "Регистрация завершена! Выполняется вход...")
            return redirect("lobby")
        else:

            return render(request, "core/login_page.html", {
                'active_tab': 'register',
                "register_form": form,
                "login_form": LoginForm()
            })
    else:

        form = RegisterForm()

    return render(request, "core/login_page.html", {
        "register_form": form,
        "login_form": LoginForm()
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect("lobby")

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data.get("user")
            if user:
                login(request, user)
                messages.success(request, "Добро пожаловать, вы вошли!")
                return redirect("lobby")

        messages.error(request, "Неверный логин или пароль.")
    else:

        form = LoginForm()

    return render(request, "core/login_page.html", {
        "login_form": form,
        "register_form": RegisterForm()
    })

def logout_view(request):

    logout(request)

    return redirect("home")

@login_required
def settings_view(request):
    profile_form = ProfileUpdateForm(instance=request.user)
    current_password_form = CurrentPasswordForm(user=request.user)
    password_form = PasswordChangeCustomForm(user=request.user)

    active_tab = "profile"
    show_new_password_form = False

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
            current_password_form = CurrentPasswordForm(request.user, request.POST)
            if current_password_form.is_valid():
                show_new_password_form = True
                active_tab = "password"
                return render(request, "core/settings_page.html", {
                    "profile_form": profile_form,
                    "current_password_form": current_password_form,
                    "password_form": password_form,
                    "active_tab": active_tab,
                    "show_new_password_form": show_new_password_form,
                })
            else:

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
                messages.error(request, "Ошибка при смене пароля.")
                active_tab = "password"
                show_new_password_form = True

        else:

            active_tab = request.POST.get("form_type", "profile")

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

@login_required
def change_password(request):
    """Смена пароля"""
    if request.method == "POST":
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
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

@login_required
def lobby_list(request):
    my_lobbies = LobbyMembership.objects.filter(user=request.user)
    return render(request, "core/lobby.html", {"my_lobbies": my_lobbies})

@login_required
def lobby_create(request):
    if request.method == "POST":
        form = LobbyCreateForm(request.POST)
        if form.is_valid():
            lobby = form.save(commit=False)
            lobby.owner = request.user
            lobby.save()
            LobbyMembership.objects.create(user=request.user, lobby=lobby, role="owner")
            messages.success(request, "Лобби успешно создано")
            return redirect("lobby")
    else:
        form = LobbyCreateForm()
    return render(request, "core/lobby_cre.html", {"form": form})

@login_required
def lobby_settings(request, lobby_id):
    lobby = get_object_or_404(Lobby, id=lobby_id)
    membership = LobbyMembership.objects.filter(user=request.user, lobby=lobby).first()

    if not membership:
        return redirect("error403")

    # только owner и admin имеют доступ к настройкам
    if membership.role not in ["owner", "admin"]:
        return redirect("error403")

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "basic_settings":
            # owner и admin могут менять основные параметры
            lobby.name = request.POST.get("lobby_name")
            lobby.is_public = "is_public" in request.POST
            lobby.is_active = "is_active" in request.POST
            lobby.save()
            messages.success(request, "Изменения сохранены.")

        elif form_type == "add_member":
            # добавлять участников может и админ, и владелец
            form = AddMemberForm(request.POST, lobby=lobby)
            if form.is_valid():
                role = form.cleaned_data.get("role")
                if membership.role == "admin" and role == "owner":
                    messages.error(request, "Администратор не может назначить владельца.")
                else:
                    form.save()
                    messages.success(request, "Участник добавлен.")
            else:
                messages.error(request, "Ошибка при добавлении участника.")

        elif form_type == "delete_confirm":
            # удалять может только владелец
            if membership.role == "owner":
                lobby.delete()
                messages.success(request, "Лобби удалено.")
                return redirect("lobby")
            else:
                messages.error(request, "Удалить может только владелец.")

        elif form_type == "update_roles":
            # обновление ролей участников
            for key, value in request.POST.items():
                if key.startswith("role_"):
                    member_id = key.split("_")[1]
                    try:
                        member = LobbyMembership.objects.get(id=member_id, lobby=lobby)
                        # нельзя менять владельца
                        if member.role == "owner":
                            continue
                        # админ не может менять роль другого админа
                        if membership.role == "admin" and member.role == "admin":
                            continue
                        member.role = value
                        member.save()
                    except LobbyMembership.DoesNotExist:
                        continue
            messages.success(request, "Роли обновлены.")

        elif form_type == "remove_member":
            member_id = request.POST.get("member_id")
            try:
                target = LobbyMembership.objects.get(id=member_id, lobby=lobby)
                if target.role != "owner":  # защита от удаления владельца
                    target.delete()
                    messages.success(request, "Участник исключён.")
                else:
                    messages.error(request, "Нельзя удалить владельца лобби.")
            except LobbyMembership.DoesNotExist:
                messages.error(request, "Участник не найден.")

    add_member_form = AddMemberForm(lobby=lobby)
    members = LobbyMembership.objects.filter(lobby=lobby).select_related("user")

    return render(request, "core/lobby_set.html", {
        "lobby": lobby,
        "add_member_form": add_member_form,
        "members": members,
        "user_role": membership.role,
    })

@login_required
def lobby_search(request):
    """Поиск лобби по коду"""
    query = request.GET.get("code")
    result = None
    if query:
        try:
            result = Lobby.objects.get(code=query, is_public=True)
        except Lobby.DoesNotExist:
            messages.error(request, "Лобби с таким кодом не найдено или оно приватное.")
    return render(request, "core/lobby.html", {"search_result": result})

@login_required
def lobby(request):

    query = request.GET.get("code", "").strip()
    error_message = None

    if query:
        try:
            lobby_obj = Lobby.objects.get(code=query, is_public=True)
            lobbies = [lobby_obj]
        except Lobby.DoesNotExist:
            lobbies = Lobby.objects.filter(memberships__user=request.user)
            error_message = "Лобби с таким идентификатором не найдено или оно приватное."
    else:
        lobbies = Lobby.objects.filter(memberships__user=request.user)

    for lb in lobbies:
        membership = LobbyMembership.objects.filter(user=request.user, lobby=lb).first()
        lb.user_role = membership.role if membership else None

    return render(request, "core/lobby.html", {
        "lobbies": lobbies,
        "search_query": query,
        "error_message": error_message,
    })

@login_required
def lobby_cre(request):

    if request.method == "POST":
        name = (request.POST.get("lobby_name") or "").strip()
        if not name:
            messages.error(request, "Введите название лобби.")
            return render(request, "core/lobby_cre.html")
        # создаём лобби, save() сам сгенерирует уникальный code
        lobby = Lobby.objects.create(name=name, owner=request.user)
        # создаём membership владельца
        LobbyMembership.objects.create(lobby=lobby, user=request.user, role="owner")
        messages.success(request, f"Лобби «{lobby.name}» создано (код: {lobby.code}).")
        return redirect("lobby")
    return render(request, "core/lobby_cre.html")

@login_required
def lobby_detail(request, lobby_id):
    lobby = get_object_or_404(Lobby, id=lobby_id)

    # Проверяем, состоит ли пользователь в лобби
    membership = LobbyMembership.objects.filter(user=request.user, lobby=lobby).first()
    if not membership:
        # пользователь не состоит в лобби → создаём как guest
        membership = LobbyMembership.objects.create(user=request.user, lobby=lobby, role="guest")

    devices = lobby.devices.all()

    return render(request, "core/lobby_detail.html", {
        "lobby": lobby,
        "devices": devices,
        "user_role": membership.role,
    })

@login_required
def lobby_leave(request, lobby_id):
    lobby = get_object_or_404(Lobby, id=lobby_id)
    membership = LobbyMembership.objects.filter(user=request.user, lobby=lobby).first()

    if not membership:
        messages.error(request, "Вы не состоите в этом лобби.")
        return redirect("lobby")

    # Владелец не может покинуть собственное лобби
    if membership.role == "owner":
        messages.error(request, "Владелец не может выйти из собственного лобби. Сначала передайте права или удалите лобби.")
        return redirect("lobby_set", lobby_id=lobby.id)

    if request.method == "POST":
        membership.delete()
        messages.success(request, f"Вы вышли из лобби «{lobby.name}».")
        return redirect("lobby")

    return redirect("lobby")

@login_required
def device_add(request, lobby_id):
    lobby = get_object_or_404(Lobby, id=lobby_id)
    membership = LobbyMembership.objects.filter(user=request.user, lobby=lobby).first()

    if not membership or membership.role == "guest":
        messages.error(request, "Гости не могут добавлять устройства.")
        return redirect("lobby_detail", lobby_id=lobby.id)

    if request.method == "POST":
        form = AddDeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.lobby = lobby
            device.save()
            messages.success(request, f"Устройство {device.name} добавлено.")
            return redirect("lobby_detail", lobby_id=lobby.id)
    else:
        form = AddDeviceForm()

    return render(request, "core/device_add.html", {"form": form, "lobby": lobby})

@login_required
def device_detail(request, lobby_id, device_id):
    lobby = get_object_or_404(Lobby, id=lobby_id)
    device = get_object_or_404(Device, id=device_id, lobby=lobby)

    membership = LobbyMembership.objects.filter(user=request.user, lobby=lobby).first()
    user_role = membership.role if membership else "guest"

    # --- Проверка доступа к устройству ---
    if device.access_roles:
        allowed_roles = device.access_roles.split(",")  # список ролей, которые имеют доступ
        if user_role not in allowed_roles:
            # Нет доступа → перенаправляем на шаблон с ошибкой
            return render(request, "core/error403.html", {
                "message": "У вас нет доступа к этому устройству.",
                "lobby": lobby,
                "device": device,
            })

    # Обработка POST для изменения ролей доступа
    if request.method == "POST" and request.POST.get("form_type") == "update_access_roles":
        if user_role in ["owner", "admin"]:
            roles = []
            for role in ["owner", "admin", "member", "guest"]:
                if request.POST.get(f"role_{role}"):
                    roles.append(role)
            # всегда гарантируем owner/admin
            if "owner" not in roles:
                roles.append("owner")
            if "admin" not in roles:
                roles.append("admin")
            device.access_roles = ",".join(roles)
            device.save()
            messages.success(request, "Права доступа к устройству обновлены.")
        else:
            messages.error(request, "У вас нет прав изменять доступ к устройствам.")

    templates = {
        "lamp": "core/device_lamp.html",
        "kettle": "core/device_kettle.html",
        "thermometer": "core/device_thermometer.html",
    }
    template = templates.get(device.device_type, "core/device_detail.html")

    return render(request, template, {
        "lobby": lobby,
        "device": device,
        "user_role": user_role,
    })

@login_required
def device_delete(request, lobby_id, device_id):
    lobby = get_object_or_404(Lobby, id=lobby_id)
    device = get_object_or_404(Device, id=device_id, lobby=lobby)
    membership = LobbyMembership.objects.filter(user=request.user, lobby=lobby).first()

    if not membership or membership.role not in ["owner", "admin"]:
        messages.error(request, "Удалять устройства могут только владелец и администраторы.")
        return redirect("lobby_detail", lobby_id=lobby.id)

    device.delete()
    messages.success(request, "Устройство удалено.")
    return redirect("lobby_detail", lobby_id=lobby.id)