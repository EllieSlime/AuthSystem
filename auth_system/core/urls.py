from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("account/", views.account, name="account"),
    path("adminn/", views.adminn, name="adminn"),
    path("assistant/", views.assistant, name="assistant"),
    path("device/", views.device, name="device"),
    path("error401/", views.error401, name="error401"),
    path("error403/", views.error403, name="error403"),
    path("login/", views.login, name="login"),
    path("settings/", views.settings, name="settings"),
    path("lobby/", views.lobby, name="lobby"),
    path("lobby_add/", views.lobby_add, name="lobby_add"),
    path("lobby_set/", views.lobby_set, name="lobby_set"),
    path("lobby_cre/", views.lobby_cre, name="lobby_cre"),
]