from django.forms import ModelForm

from project.style.models import Site, Style

class StyleForm(ModelForm):
    class Meta:
        model = Style
        fields = ["name", "logo", "site", "description", "source"]
        # labels = {
        #     "name": "Название",
        #     "logo": "Логотип",
        #     "site": "Сайт",
        #     "description": "Описание",
        #     "source": "CSS"
        # }
