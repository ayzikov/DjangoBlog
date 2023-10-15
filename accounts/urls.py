# файлы проекта
from . import views

# импорты джанго
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),

    # redirect_authenticated_user=True означает что, если пользователь после аутентификации пытается получить
    # доступ к .../login/ , то он будет перенаправлен на адрес "LOGIN_REDIRECT_URL" определенный в settings.py
    path('login/', views.CustomLoginView.as_view(redirect_authenticated_user=True), name='login'),

    # тут мы изменяем класс, который отвечает за выход пользователя из системы добавляя ему шаблон
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    path('profile/', views.profile, name='profile'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change')
]

app_name = 'accounts'