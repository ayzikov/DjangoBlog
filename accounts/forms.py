# импорты проекта
from .models import Profile

# импорты джанго
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django_summernote.widgets import SummernoteWidget


class CustomUserCreationForm(UserCreationForm):
    ''' Класс для создания формы регистрации пользователя '''
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput())

    class Meta:
        model = User
        # порядок в котором высвечиваются поля в форме
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class CustomLoginForm(AuthenticationForm):
    ''' Класс для создания формы входа пользователя в систему '''

    # attrs={'placeholder': 'введите имя пользователя'} задает значение которое будет отображаться в виде
    # серого текста в поле формы перед тем как пользователь начнет вводить туда свои данные
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'введите имя пользователя'}))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'введите пароль'}))

    # initial=True указывает начальное значение для этого поля
    remember_me = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'remember_me')


class UpdateProfileForm(forms.ModelForm):
    ''' Обновление профиля пользователя '''
    avatar = forms.ImageField(widget=forms.FileInput())
    bio = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class UpdateUserForm(forms.ModelForm):
    ''' Обновление информации о пользователе '''
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())
    email = forms.EmailField(required=True,
                             widget=forms.TextInput())

    class Meta:
        model = User
        fields = ['username', 'email']