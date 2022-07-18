"""
dasist.invarch.urls
"""

from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('',                  login_required(views.ScanList.as_view()), name='scan_list'),
    #path('lpp/<int:lpp>/', views.scan_set_lpp, name='scan_set_lpp'),
    #path('filter/',           views.scan_set_filter, name='scan_set_filter'),
    #path('get_subjs/',        views.scan_get_subjects, name='scan_get_subjects'),
    # path('a/',              views.scan_add),
    #path('<int:pk>/',      login_required(views.ScanDetail.as_view()), name='scan_view'),
    #path('<int:pk>/u/',    views.scan_edit, name='scan_edit'),
    #path('<int:pk>/d/',    views.scan_delete, name='scan_delete'),
    #path('clean_spaces/',     views.scan_clean_spaces, name='scan_clean_spaces'),
    #path('replace_depart/',   views.scan_replace_depart, name='scan_replace_depart'),
    #path('replace_place/',    views.scan_replace_place, name='scan_replace_place'),
]
