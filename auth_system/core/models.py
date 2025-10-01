from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
import string
import random
User = settings.AUTH_USER_MODEL

ICON_CHOICES = [
    ("fa-house-user", "Дом"),
    ("fa-building", "Здание"),
    ("fa-home", "Home"),
]


def _generate_code():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=6))

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

def generate_lobby_code():
    """Генерация случайного 6-значного кода"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Lobby(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=6, unique=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_lobbies")
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default="fa-house-user")
    is_public = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.code})"

    def save(self, *args, **kwargs):
        # Генерируем уникальный код при первом сохранении
        if not self.code:
            while True:
                code = _generate_code()
                if not Lobby.objects.filter(code=code).exists():
                    self.code = code
                    break
        # если иконка не задана, можно присвоить случайную
        if not self.icon:
            self.icon = random.choice([c[0] for c in ICON_CHOICES])
        super().save(*args, **kwargs)


class LobbyMembership(models.Model):
    ROLE_CHOICES = [
        ("owner", "Владелец"),
        ("admin", "Администратор"),
        ("member", "Участник"),
        ("guest", "Гость"),
    ]
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lobby_memberships")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("lobby", "user")

    def __str__(self):
        return f"{self.user} @ {self.lobby} ({self.role})"


class Device(models.Model):
    DEVICE_TYPES = [
        ("kettle", "Чайник"),
        ("thermometer", "Термометр"),
        ("lamp", "Лампочка"),
    ]

    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name="devices")
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    created_at = models.DateTimeField(default=timezone.now)

    # активное ли устройство (например, если лобби отключено)
    is_active = models.BooleanField(default=True)

    # ✅ по умолчанию — доступ всем кроме гостей
    access_roles = models.CharField(
        max_length=100,
        default="owner,admin,member"
    )
    def roles_list(self):
        """Разбивает строку access_roles в список ролей"""
        return [r.strip() for r in self.access_roles.split(",") if r.strip()]

    def __str__(self):
        return f"{self.name} ({self.get_device_type_display()})"

