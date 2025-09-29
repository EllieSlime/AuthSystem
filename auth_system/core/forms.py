from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password


class RegisterForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Ваше полное имя"
        }),
        label="ФИО",
        error_messages={
            "required": "Пожалуйста, введите ваше имя",
            "max_length": "Имя слишком длинное",
        }
    )

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
        fields = ("email",)
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-input",
                "placeholder": "Ваш email"
            }),

        }
        labels = {
            "email": "Email",
        }
        error_messages = {
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

class ProfileUpdateForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        label="ФИО",
        widget=forms.TextInput(attrs={"class": "form-input"})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        label="Телефон",
        widget=forms.TextInput(attrs={"class": "form-input"})
    )
    address = forms.CharField(
        max_length=255,
        required=False,
        label="Адрес",
        widget=forms.TextInput(attrs={"class": "form-input"})
    )

    class Meta:
        model = User
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance") or getattr(self, "instance", None)

        if instance and instance.pk:
            self.fields["full_name"].initial = getattr(instance, "first_name", "")
            self.fields["email"].initial = getattr(instance, "email", "")
            if hasattr(instance, "phone"):
                self.fields["phone"].initial = getattr(instance, "phone", "")
            if hasattr(instance, "address"):
                self.fields["address"].initial = getattr(instance, "address", "")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("full_name", "")
        if hasattr(user, "phone"):
            user.phone = self.cleaned_data.get("phone", "")
        if hasattr(user, "address"):
            user.address = self.cleaned_data.get("address", "")
        if commit:
            user.save()
        return user


class PasswordChangeCustomForm(forms.Form):
    current_password = forms.CharField(
        label="Текущий пароль",
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
        error_messages={"required": "Введите текущий пароль"}
    )
    new_password = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
        validators=[validate_password],
        error_messages={"required": "Введите новый пароль"}
    )
    confirm_password = forms.CharField(
        label="Подтверждение нового пароля",
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
        error_messages={"required": "Подтвердите новый пароль"}
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_current_password(self):
        current_password = self.cleaned_data.get("current_password")
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Неверный текущий пароль.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error("confirm_password", "Пароли не совпадают.")
        return cleaned_data
