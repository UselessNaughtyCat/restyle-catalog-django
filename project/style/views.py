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
    sort = None

    def get(self, request, *args, **kwargs):
        if not request.GET.get("site", "") is None:
            self.site_name = request.GET.get("site", "")
        if not request.GET.get("sort", "") is None:
            self.sort = request.GET.get("sort", "")
        return super(StyleListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StyleListView, self).get_context_data(**kwargs)
        context["sites"] = Site.objects.order_by("id")[:3]
        sort = "-id"
        if self.sort in ["id", "-average_rating", "-subscribed"]:
            sort = self.sort
        if self.site_name:
            curr_site = Site.objects.get(name=self.site_name)
            context['styles'] = Style.objects.filter(site=curr_site).order_by(sort)
        else:
            context['styles'] = Style.objects.all().order_by(sort)
        context['sort_list'] = {"-average_rating" : "Top rated", "-subscribed" : "Top subscribed", "id" : "First added"}
        return context

class StyleInfoView(TemplateView):
    template_name = "style/info.html"
    style = None
    person_is_subscibed = False
    person_is_current = False

    def get(self, request, *args, **kwargs):
        self.style = Style.objects.get(pk=self.kwargs["style_id"])
        if request.user.is_authenticated:
            self.person_is_current = request.user == self.style.creator.user
            if self.style in request.user.person.subscriptions.all():
                self.person_is_subscibed = True
        return super(StyleInfoView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StyleInfoView, self).get_context_data(**kwargs)
        context['style'] = self.style
        context['person_is_current'] = self.person_is_current
        context['person_is_subscibed'] = self.person_is_subscibed
        return context

class StyleCreate(CreateView):
    model = Style
    form_class = StyleForm
    template_name = "style/edit.html"
    success_url = "/"
    new_site = None

    def get_context_data(self, **kwargs):
        context = super(StyleCreate, self).get_context_data(**kwargs)
        context['title'] = "Create style"
        context['is_create'] = True
        context['is_update'] = False
        return context

    def post(self, request, *args, **kwargs):
        self.new_site = Style.get_new_site(request.POST.get("site_name", ""), request.POST.get("site_urls", ""))
        return super(StyleCreate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.creator = self.request.user.person
        if not self.new_site is None:
            form.instance.site = self.new_site
        return super().form_valid(form)

class StyleUpdate(UpdateView):
    model = Style
    form_class = StyleForm
    template_name = "style/edit.html"
    pk_url_kwarg = "style_id"
    success_url = "/"
    new_site = None

    def get(self, request, *args, **kwargs):
        style = Style.objects.get(id=self.kwargs["style_id"])
        if not request.user is None:
            if request.user != style.creator.user:
                return redirect('style-info', style_id=style.id)
            else:
                return super(StyleUpdate, self).get(request, *args, **kwargs)
        else:
            return super(StyleUpdate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.new_site = Style.get_new_site(request.POST.get("site_name", ""), request.POST.get("site_urls", ""))
        return super(StyleUpdate, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StyleUpdate, self).get_context_data(**kwargs)
        context['title'] = "Update style"
        context['is_create'] = False
        context['is_update'] = True
        return context

    def form_valid(self, form):
        if not self.new_site is None:
            form.instance.site = self.new_site
        return super().form_valid(form)

class StyleDelete(DeleteView):
    model = Style
    form_class = StyleForm
    template_name = "style/remove.html"
    pk_url_kwarg = "style_id"
    success_url = "/"

    def get(self, request, *args, **kwargs):
        style = Style.objects.get(id=self.kwargs["style_id"])
        if not request.user is None:
            if request.user != style.creator.user:
                return redirect('style-info', style_id=style.id)
            else:
                return super(StyleDelete, self).get(request, *args, **kwargs)
        else:
            return super(StyleDelete, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StyleDelete, self).get_context_data(**kwargs)
        context['style'] = Style.objects.get(id=self.kwargs["style_id"])
        return context
