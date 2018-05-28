from django.views.generic.base import TemplateView

from project.style.models import Style

class MainView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context["styles_high_rate"] = Style.objects.order_by("-average_rating")[:4]
        context["styles_many_subs"] = Style.objects.order_by("-subscribed")[:4]
        context["styles_last_added"] = Style.objects.order_by("-id")[:4]
        return context
