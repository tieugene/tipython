"""
invoice.urls
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.InvoiceList.as_view(), name='invoice_list'),
    path('lpp/<int:lpp>/', views.invoice_set_lpp, name='invoice_set_lpp'),
    path('mode/<int:mode>/', views.invoice_set_mode, name='invoice_set_mode'),
    path('fs/', views.invoice_filter_state, name='invoice_filter_state'),
    path('get_subjs/', views.invoice_get_subjects, name='invoice_get_subjects'),
    path('a/', views.invoice_add, name='invoice_add'),  # GET/POST; ACL: assign, Cancel > list; save > view (Draft)
    path('<int:pk>/', views.invoice_view, name='invoice_view'),  # GET; ACL: assign|approv
    path('<int:pk>/u/', views.invoice_edit, name='invoice_edit'),  # GET/POST; ACL: assign+draft;
    path('<int:pk>/ru/', views.invoice_reedit, name='invoice_reedit'),  # GET/POST; ACL: assign+draft?;
    path('<int:pk>/d/', views.invoice_delete, name='invoice_delete'),  # GET; ACL: assign;
    path('<int:pk>/s/', views.invoice_toscan, name='invoice_toscan'),
    path('<int:pk>/r/', views.invoice_restart, name='invoice_restart'),
    path('<int:pk>/id/', views.invoice_img_del, name='invoice_img_del'),
    path('<int:pk>/iup/', views.invoice_img_up, name='invoice_img_up'),
    path('<int:pk>/idn/', views.invoice_img_dn, name='invoice_img_dn'),
    path('<int:pk>/irl/', views.invoice_img_rl, name='invoice_img_rl'),
    path('<int:pk>/irr/', views.invoice_img_rr, name='invoice_img_rr'),
    path('<int:pk>/mail/', views.invoice_mail, name='invoice_mail'),
    # path('<int:pk>/g/$', 'invoice_get'),  # GET; ACL: assign;
]
