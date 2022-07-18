"""
core.urls
"""

from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = (
    path('o/',                    login_required(views.OrgList.as_view()), name='org_list'),
    path('o/<int:pk>/',      login_required(views.OrgDetail.as_view()), name='org_view'),
    path('o/<int:pk>/u/',      views.org_edit, name='org_edit'),
    path('o/get_by_inn/',         views.org_get_by_inn, name='org_get_by_inn'),
    re_path('org-autocomplete/$',       views.OrgAutocomplete.as_view(), name='org-autocomplete',),
)
