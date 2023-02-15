from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    name = forms.CharField(max_length=200,
                           widget=forms.TextInput(attrs={"class": "username__input", "placeholder": "Как к вам можно обращаться?"}))
    phone_number = forms.CharField(max_length=12, widget=forms.TextInput(
        attrs={"class": "contact__input", "placeholder": "Укажите ваши контакты"}))
    comment = forms.CharField(max_length=12, widget=forms.Textarea(
        attrs={"class": "contact__input", "placeholder": "Комментарии"}))

    class Meta:
        model = Application
        fields = [
            "name",
            "phone_number",
            "comment"
        ]
