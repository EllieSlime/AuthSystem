from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Придумайте пароль"
        }),
        label="Пароль"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Повторите пароль"
        }),
        label="Повторите пароль"
    )

    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Ваше полное имя"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-input",
                "placeholder": "Ваш email"
            }),

        }
        labels = {
            "username": "ФИО",
            "email": "Email",
        }
        error_messages = {
            "username": {
                "max_length": "Имя слишком длинное",
            },
            "email": {
                "invalid": "Введите корректный адрес email",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if "class" not in field.widget.attrs:
                field.widget.attrs["class"] = "form-input"

    def clean_password2(self):
        cd = self.cleaned_data
        #print("RegisterForm.clean_password2 вызван. cd =", cd)
        if cd.get("password") != cd.get("password2"):
            #print("⚠️ Пароли не совпадают")
            self.add_error("password", "Пароли не совпадают!")
            return
            #raise forms.ValidationError("Пароли не совпадают!")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        #print("RegisterForm.clean_email вызван. email =", email)
        if User.objects.filter(email=email).exists():
            #print("⚠️ Email уже занят:", email)
            self.add_error("email", "Пользователь с таким email уже зарегистрирован.")
            return
            #raise forms.ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-input",
            "placeholder": "Ваш email"
        }),
    error_messages={
        "invalid": "Введите корректный адрес электронной почты."
    }
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Ваш пароль"
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label="Запомнить меня"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "remember_me" and "class" not in field.widget.attrs:
                field.widget.attrs["class"] = "form-input"

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        #print("LoginForm.clean вызван. email:", email, "| password:", password)

        if email and password:
            try:
                user_obj = User.objects.get(email=email)
                #print("Пользователь найден:", user_obj.username)
            except User.DoesNotExist:
                #print("⚠️ Пользователь с email", email, "не найден")
                #raise forms.ValidationError("Пользователь с таким email не найден.")
                self.add_error("email", "Пользователь с таким email не найден.")
                return

            user = authenticate(username=user_obj.username, password=password)
            #print("authenticate вернул:", user)

            if user is None:
                #print("⚠️ Неверный пароль для email:", email)
                #raise forms.ValidationError("Неверный пароль.")
                self.add_error("password", "Неверный пароль.")
                return

            cleaned_data["user"] = user
            print("✅ Авторизация успешна. user =", user)

        return cleaned_data

