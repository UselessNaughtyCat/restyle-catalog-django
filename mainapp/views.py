from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.http import HttpResponse

from mainapp.models import Style, Site

def hello(request):
    return HttpResponse("U EXPECT SOME HELLO SHIT?<BR><H1>GTFO</H1>")

class MainView(TemplateView):
    template_name = "mainpage.html"

class SiteListView(TemplateView):
    template_name = "site_catalog.html"

    def get_context_data(self, **kwargs):
        context = super(SiteListView, self).get_context_data(**kwargs)
        context["sites"] = Site.objects.all()
        return context

class StyleListView(TemplateView):
    template_name = "style_catalog.html"

    def get_context_data(self, **kwargs):
        context = super(StyleListView, self).get_context_data(**kwargs)
        context['styles'] = Style.objects.all()
        return context

class StyleInfoView(TemplateView):
    template_name = "style_info.html"
    style = 0

    def get(self, request, *args, **kwargs):
        self.style = self.kwargs["style_id"]
        return super(StyleInfoView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StyleInfoView, self).get_context_data(**kwargs)
        context['style'] = Style.objects.get(id=self.style)
        return context

class ProfileInfoView(TemplateView):
    template_name = "person_info.html"
    person_id = None
    is_self_person = False

    def get(self, request, *args, **kwargs):
        self.person_id = self.kwargs["person_id"]
        self.is_self_person = int(request.user.id) == int(self.kwargs["person_id"])
        return super(ProfileInfoView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileInfoView, self).get_context_data(**kwargs)
        current_user = User.objects.get(id=self.person_id)
        context['user'] = current_user
        context['sub_styles'] = current_user.person.subscriptions.all()
        context['user_styles'] = Style.objects.filter(creator=current_user.id)
        context['is_self_person'] = self.is_self_person
        return context
