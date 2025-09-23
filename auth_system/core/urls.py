from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("account/", views.account, name="account"),
    path("admin/", views.admin, name="admin"),
    path("assistant/", views.assistant, name="assistant"),
    path("device/", views.device, name="device"),
    path("error401/", views.error401, name="error401"),
    path("error403/", views.error403, name="error403"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("settings/", views.settings, name="settings"),
]