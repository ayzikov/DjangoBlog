# импорты проекта
from .models import Profile

# импорты джанго
from django import forms
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django_summernote.widgets import SummernoteWidget

from PIL import Image
from io import BytesIO


class CustomUserCreationForm(UserCreationForm):
    ''' Класс для создания формы регистрации пользователя '''
    first_name = forms.CharField(max_length=100,
                                 widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Имя'}))

    last_name = forms.CharField(max_length=100,
                                widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Фамилия'}))

    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(
                                   attrs={"class": "form-control mb-1", 'placeholder': 'Имя пользователя'}))

    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Email'}))

    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={"class": "form-control mb-1", 'placeholder': 'Пароль'}))

    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={"class": "form-control mb-1", 'placeholder': 'Подтверждение пароля'}))

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
                               widget=forms.TextInput(
                                   attrs={"class": "form-control mb-1", 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(
                                   attrs={"class": "form-control mb-1", 'placeholder': 'Пароль'}))

    # initial=True указывает начальное значение для этого поля
    remember_me = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'remember_me')


class UpdateProfileForm(forms.ModelForm):
    ''' Обновление профиля пользователя '''
    avatar = forms.ImageField(required=False,
                              widget=forms.FileInput())
    bio = forms.CharField(required=False,
                          widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '350px'}}))

    # Переопределяем метод save чтобы изображение загруженное пользователем не теряло качество
    def save(self, commit=True):
        # Сохраняем экземпляр формы без сохранения в базе данных
        instance = super().save(commit=False)

        # Проверяем, есть ли изображение в форме
        if self.cleaned_data['avatar']:
            # Открываем изображение
            avatar = Image.open(self.cleaned_data['avatar'])
            if avatar.height > 300 or avatar.width > 300:
                output_size = (300, 300)
                avatar.thumbnail(output_size)

                # Создание файла из изображения который можно сохранить в джанго
                avatar_io = BytesIO()

                # Сохраняем изображение в объект BytesIO
                avatar.save(avatar_io, format='JPEG', quality=90)

                # Сохраняем изображение в поле avatar экземпляра формы
                instance.avatar.save(f'{instance.user.username}_avatar.jpg', File(avatar_io), save=False)

        if commit:
            instance.save()

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class UpdateUserForm(forms.ModelForm):
    ''' Обновление информации о пользователе '''
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())
    first_name = forms.CharField(max_length=100,
                                 required=False,
                                 widget=forms.TextInput())
    last_name = forms.CharField(max_length=100,
                                required=False,
                                widget=forms.TextInput())
    email = forms.EmailField(required=True,
                             widget=forms.TextInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
