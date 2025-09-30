from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.get(email="test22@example.com")
user.is_active = True
user.save()
print("Аккаунт снова активирован")