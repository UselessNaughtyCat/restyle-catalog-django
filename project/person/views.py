from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect

from project.person import forms
from project.style.models import Style

class PersonInfoView(TemplateView):
    template_name = "person/info.html"
    person = None
    is_current = False

    def get(self, request, *args, **kwargs):
        self.person = User.objects.get(id=self.kwargs["person_id"]).person
        if not request.user is None:
            if not request.user.is_anonymous:
                self.is_current = request.user == self.person.user
        return super(PersonInfoView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PersonInfoView, self).get_context_data(**kwargs)
        context['person'] = self.person
        context['person_subs'] = self.person.subscriptions.all()
        context['person_works'] = Style.objects.filter(creator=self.person)
        context['person_is_current'] = self.is_current
        return context

class RegisterFormView(CreateView):
    form_class = forms.RegisterForm
    success_url = "/login/"
    template_name = "person/register.html"

class LoginFormView(FormView):
    form_class = forms.LoginForm
    template_name = "person/login.html"
    success_url = "/"

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super(LoginFormView, self).form_valid(form)

class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect("/")
