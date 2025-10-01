from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("adminn/", views.adminn, name="adminn"),
    path("assistant/", views.assistant, name="assistant"),

    path("error401/", views.error401, name="error401"),
    path("error403/", views.error403, name="error403"),
    path("login_page/", views.login_page, name="login_page"),
    path("deactivate/", views.deactivate_profile, name="deactivate_profile"),
    path("lobby/<int:lobby_id>/leave/", views.lobby_leave, name="lobby_leave"),
    path("lobby_add/", views.lobby_add, name="lobby_add"),

    path("lobby_cre/", views.lobby_cre, name="lobby_cre"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("settings/", views.settings_view, name="settings"),
    path("settings/update-profile/", views.update_profile, name="update_profile"),
    path("settings/change-password/", views.change_password, name="change_password"),



    path("lobby/search/", views.lobby_search, name="lobby_search"),

    path("lobby/", views.lobby, name="lobby"),
    path("lobby/create/", views.lobby_cre, name="lobby_cre"),
    # placeholder для настроек и входа в лобби (можно реализовать позже)
    path("lobby/<int:lobby_id>/settings/", views.lobby_settings, name="lobby_set"),
    path("lobby/<int:lobby_id>/", views.lobby_detail, name="lobby_detail"),

    path("lobby/<int:lobby_id>/device/add/", views.device_add, name="device_add"),
    path("lobby/<int:lobby_id>/device/<int:device_id>/", views.device_detail, name="device_detail"),
    path("lobby/<int:lobby_id>/device/<int:device_id>/delete/", views.device_delete, name="device_delete"),
]