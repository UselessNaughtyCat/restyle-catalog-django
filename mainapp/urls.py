from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('sites/', views.SiteListView.as_view(), name='sites'),
    re_path(r'styles/(?:(?P<site_name>\w+)/)?$', views.StyleListView.as_view(), name='styles'),
    path('style/<int:style_id>', views.StyleInfoView.as_view(), name='style-info'),
    path('person/<int:person_id>', views.PersonInfoView.as_view(), name='person'),

    path('style/add', login_required(views.StyleCreate.as_view()), name='style-add'),
    path('style/<int:style_id>/update', login_required(views.StyleUpdate.as_view()), name='style-update'),

    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': 'main'}, name='logout'),

    path('hello/', views.hello, name='hello')
]
