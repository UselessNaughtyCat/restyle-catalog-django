from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from project.person.models import Person
from django.utils.translation import ugettext_lazy as _

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "first_name", "last_name"]
        labels = {
            'username': _('Логин'),
            "email": _('E-Mail'), 
            "password1": _('Пароль'), 
            "password2": _('Подтверждение пароля'), 
            "first_name": _('Имя'), 
            "last_name": _('Фамилия')
        }
        help_texts = {
            'username': _("Обязательное поле. 150 символов или меньше. Буквы, цифры и символы '@', '.', '+', '-', '_'."),
        }
        # error_messages = {
        #     'name': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            Person.objects.create(user=user)
        return user

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})