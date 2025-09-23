from django.shortcuts import render

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
def login(request):
    return render(request, "core/login.html")
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


