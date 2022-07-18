"""
dasist.contrarch.urls
"""

from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = (
    path('',                  login_required(views.ContrarchList.as_view()), name='contrarch_list'),
    path('<int:pk>/',      login_required(views.ContrarchDetail.as_view()), name='contrarch_view'),
    path('lpp/<int:lpp>/', views.contrarch_set_lpp, name='contrarch_set_lpp'),
    path('filter/',           views.contrarch_set_filter, name='contrarch_set_filter'),
    path('get_subjs/',        views.contrarch_get_subjects, name='contrarch_get_subjects'),
)
