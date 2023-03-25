from django import forms
from .models import Application, UserAdditionalInfo, Order
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class ApplicationForm(forms.ModelForm):
    name = forms.CharField(max_length=200,
                           widget=forms.TextInput(
                               attrs={"class": "name_input", "placeholder": "Введите ваше имя"}))
    phone_number = forms.CharField(max_length=12, widget=forms.TextInput(
        attrs={"class": "phone_number_input", "placeholder": "Введите ваш номер"}))
    comment = forms.CharField(max_length=250, widget=forms.TextInput(
        attrs={"class": "comment_input", "placeholder": "Опишите задачу"}))

    class Meta:
        model = Application
        fields = [
            "name",
            "phone_number",
            "comment"
        ]


class UserRegistrationsForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autocomplete": "username", "class": "username__input",
                                                             "placeholder": "Введите имя пользователя"}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={"autocomplete": "name", "class": "name__input", "placeholder": "Как к вам можно обращаться?"}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={"autocomplete": "email", "class": "email__input", "placeholder": "Введите email"}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "password__input", "placeholder": "Введите пароль"}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "password__input",
                                          "placeholder": "Введите пароль ещё раз"}),
    )

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'email',
                  'password1',
                  'password2'
                  ]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'username__input', 'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"autocomplete": "password", 'class': "password__input", 'placeholder': "Введите пароль"}),
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class UserAdditionalInfoForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'username__input', 'placeholder': 'Введите телефон для связи'}))
    address = forms.CharField(required=False, max_length=250, widget=forms.Textarea(
        attrs={"class": "contact__input", "placeholder": "Ваш адрес"}))

    class Meta:
        model = UserAdditionalInfo
        fields = ("phone_number", "address")


class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


class OrderForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'username__input', 'placeholder': 'Введите телефон для связи'}))
    address = forms.CharField(required=False, max_length=250, widget=forms.Textarea(
        attrs={"class": "contact__input", "placeholder": "Адресс доставки"}))
    delivery_date = forms.DateTimeField(label="Дата доставки", widget=MyDateInput(
        attrs={"class": "date_input", }))
    comment = forms.CharField(max_length=250, widget=forms.Textarea(
        attrs={"class": "comment_input", "placeholder": "Комментарии"}))

    class Meta:
        model = Order
        fields = ("phone_number", "address", "delivery_date", "comment")
