# -*- coding: utf-8 -*-
"""
contract.urls
"""

from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('',                      login_required(views.ContractList.as_view()), name='contract_list'),
    path('lpp/<int:lpp>/',     views.contract_set_lpp, name='contract_set_lpp'),
    path('mode/<int:mode>/',   views.contract_set_mode, name='contract_set_mode'),
    path('fs/',                   views.contract_filter_state, name='contract_filter_state'),
    path('get_subjs/',            views.contract_get_subjects, name='contract_get_subjects'),
    path('a/',                    views.contract_add, name='contract_add'),  # GET/POST; ACL: assign, Cancel > list; save > view (Draft)
    path('<int:pk>/',          views.contract_view, name='contract_view'),         # GET; ACL: assign|approv
    path('<int:pk>/u/',        views.contract_edit, name='contract_edit'),         # GET/POST; ACL: assign+draft;
    path('<int:pk>/d/',        views.contract_delete, name='contract_delete'),     # GET; ACL: assign;
    path('<int:pk>/r/',        views.contract_restart, name='contract_restart'),
    path('<int:pk>/id/',       views.contract_img_del, name='contract_img_del'),
    path('<int:pk>/iup/',      views.contract_img_up, name='contract_img_up'),
    path('<int:pk>/idn/',      views.contract_img_dn, name='contract_img_dn'),
    path('<int:pk>/mail/',     views.contract_mail, name='contract_mail'),
    path('<int:pk>/a/',        views.contract_toarch, name='contract_toarch'),
    # path('<int:pk>/g/',       'contract_get'),  # GET; ACL: assign;
]
