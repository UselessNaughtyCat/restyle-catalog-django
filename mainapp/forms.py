from django.forms import ModelForm

from .models import Style, Site

class StyleForm(ModelForm):
    class Meta:
        model = Style
        fields = ["name", "image", "site", "description", "css_src"]
        labels = {
            "name": "Название",
            "image": "Логотип",
            "site": "Сайт",
            "description": "Описание",
            "css_src": "CSS"
        }
