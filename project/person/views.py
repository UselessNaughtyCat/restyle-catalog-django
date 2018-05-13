from django.views.generic.base import TemplateView
from django.contrib.auth.models import User

from project.person.models import Person
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
