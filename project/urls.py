"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from project.main.views import MainView
from project.person import views as persons
from project.style import views as styles
from project.events import views as events

urlpatterns = [
    path('', MainView.as_view(), name='main'),

    path('sites/', styles.SiteListView.as_view(), name='sites'),
    path('styles/', styles.StyleListView.as_view(), name='styles'),
    path('style/<int:style_id>', styles.StyleInfoView.as_view(), name='style-info'),
    path('style/add', login_required(styles.StyleCreate.as_view()), name='style-add'),
    path('style/<int:style_id>/update', login_required(styles.StyleUpdate.as_view()), name='style-update'),
    path('style/<int:style_id>/delete', login_required(styles.StyleDelete.as_view()), name='style-delete'),

    path('person/<int:person_id>', persons.PersonInfoView.as_view(), name='person'),
    path('register/', persons.RegisterFormView.as_view(), name='register'),
    path('login/', persons.LoginFormView.as_view(), name='login'),
    path('logout/', persons.LogoutView.as_view(), name='logout'),

    path('ajax/subscription', events.subscription),

    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
