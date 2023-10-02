# файлы проекта
from .forms import CustomUserCreationForm, CustomLoginForm

# файлы джанго
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib import messages


class SignUpView(generic.CreateView):
    ''' Представление для регистрации пользователя '''

    # Форма которая выводится при использовании представления
    form_class = CustomUserCreationForm

    # При успешной регистрации пользователь перенаправляется на страницу для входа в систему (registration/login.html)
    success_url = reverse_lazy("login")

    # имя шаблона который использует представление
    template_name = "registration/signup.html"

    # атрибут для задания начальных значений в полях формы (на данный момент не используется)
    initial = None

    def dispatch(self, request, *args, **kwargs):
        '''
        Если пользователь попытается зайти на страницу регистрации после авторизации, то будет перенаправлен
        на главную страницу блога
        '''

        if request.user.is_authenticated:
            return redirect(to='/blog/')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        ''' Если представление получает get запрос, то оно выводит форму для регистрации '''

        # создаем форму и если атрибут initial не пустой, то поля которые указанны в атрибуте будут заполнены
        # значениями. Например: {'имя поля формы': значение которое будет по дефолту}
        form = self.form_class(initial=self.initial)
        return render(request=request,
                      template_name=self.template_name,
                      context={'form': form})

    def post(self, request, *args, **kwargs):
        ''' Если представление получает post запрост, то регистрирует пользователя и выводит ему начальную страницу '''

        # записываем в форму данные, которые ввел пользователь
        form = self.form_class(request.POST)

        # проверяем заполнение формы на правильность
        if form.is_valid():
            # созраняем данные введенные пользователем в БД
            form.save()

            # получаем имя пользователя из БД
            username = form.cleaned_data.get('username')

            # выводит исчезающее уведомление на страницу пользователя с сообщением
            messages.success(request=request,
                             message=f'{username}, Ваш аккаунт успешно создан!')

            # после регистрации переводит пользователя на страницу для входа в профиль
            return redirect(to='login')

        return render(request=request,
                      template_name=self.template_name,
                      context={'form': form})


class CustomLoginView(LoginView):
    ''' Представление для обработки формы входа пользователя в систему '''

    # форма которая используется для обработки
    form_class = CustomLoginForm

    # имя шаблона для данного представления
    template_name = 'registration/login.html'

    def form_valid(self, form):
        ''' метод вызывается при успешной валидации формы '''
        remember_me = form.cleaned_data.get('remember_me')

        # если пользователь не поставил галочку "Запомнить меня"
        if not remember_me:

            # устанавливаем время сеанса == 0, это автоматически закроет сеанс после закрытия браузера
            self.request.session.set_expiry(0)

            # сохраняем сессию, так как джанго сохраняет сессию автоматически только при ее создании,
            # а мы установили для нее значение == 0 и нужно это сохранить
            self.request.session.modified = True

        # в противном случае сеанс браузера будет таким же как время сеанса cookie "SESSION_COOKIE_AGE",
        # определенное в settings.py
        return super().form_valid(form)











