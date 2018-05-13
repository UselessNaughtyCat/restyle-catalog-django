from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect

from project.style.models import Site, Style
from project.style.forms import StyleForm

class SiteListView(TemplateView):
    template_name = "style/sites.html"
    
    def get_context_data(self, **kwargs):
        context = super(SiteListView, self).get_context_data(**kwargs)
        context["sites"] = Site.objects.all()
        return context

class StyleListView(TemplateView):
    template_name = "style/catalog.html"
    site_name = None

    def get(self, request, *args, **kwargs):
        if not request.GET.get("site", "") is None:
            self.site_name = request.GET.get("site", "")

        return super(StyleListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StyleListView, self).get_context_data(**kwargs)
        if self.site_name:
            curr_site = Site.objects.get(name=self.site_name)
            context['styles'] = Style.objects.filter(site=curr_site).order_by("-upload_date")
        else:
            context['styles'] = Style.objects.all().order_by("-upload_date")

        return context

class StyleInfoView(TemplateView):
    template_name = "style/info.html"
    style = None
    is_person_subscibed = False
    is_self_person = False

    def get(self, request, *args, **kwargs):
        self.style = Style.objects.get(pk=self.kwargs["style_id"])
        if not request.user is None:
            if not request.user.is_anonymous:
                self.is_self_person = request.user == self.style.creator.user
                if self.style in request.user.person.subscriptions.all():
                    self.is_person_subscibed = True
        return super(StyleInfoView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StyleInfoView, self).get_context_data(**kwargs)
        context['style'] = self.style
        context['is_self_person'] = self.is_self_person
        context['is_person_subscibed'] = self.is_person_subscibed
        return context

class StyleCreate(CreateView):
    model = Style
    form_class = StyleForm
    template_name = "style/edit.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super(StyleCreate, self).get_context_data(**kwargs)
        context['title'] = "Добавить стиль"
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user.person
        return super().form_valid(form)

class StyleUpdate(UpdateView):
    model = Style
    form_class = StyleForm
    template_name = "style/edit.html"
    pk_url_kwarg = "style_id"
    success_url = "/"

    def get(self, request, *args, **kwargs):
        style = Style.objects.get(id=self.kwargs["style_id"])
        if not request.user is None:
            if request.user != style.creator.user:
                return redirect('style-info', style_id=style.id)
            else:
                return super(StyleUpdate, self).get(request, *args, **kwargs)
        else:
            return super(StyleUpdate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StyleUpdate, self).get_context_data(**kwargs)
        context['title'] = "Изменить стиль"
        return context

class StyleDelete(DeleteView):
    model = Style
    form_class = StyleForm
    template_name = "style/remove.html"
    pk_url_kwarg = "style_id"
    success_url = "/"

    def get(self, request, *args, **kwargs):
        style = Style.objects.get(id=self.kwargs["style_id"])
        if not request.user is None:
            if request.user != style.creator:
                return redirect('style-info', style_id=style.id)
            else:
                return super(StyleDelete, self).get(request, *args, **kwargs)
        else:
            return super(StyleDelete, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StyleDelete, self).get_context_data(**kwargs)
        context['style'] = Style.objects.get(id=self.kwargs["style_id"])
        return context
