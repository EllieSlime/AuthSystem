from django.shortcuts import render

def home(request):
    return render(request, "core/home.html")
def about(request):
    return render(request, "core/about.html")
def account(request):
    return render(request, "core/account.html")
def admin(request):
    return render(request, "core/admin.html")
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
def register(request):
    return render(request, "core/register.html")
def settings(request):
    return render(request, "core/settings.html")


