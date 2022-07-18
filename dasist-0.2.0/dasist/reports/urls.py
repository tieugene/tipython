"""
dasist.reports.urls
"""
from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = (
    path('^ledger/',                               login_required(views.LedgerList.as_view()), name='ledger_list'),
    path('^ledger/lpp/<int:lpp>/',              views.ledger_set_lpp, name='ledger_set_lpp'),
    path('^ledger/filter/',                        views.ledger_set_filter, name='ledger_set_filter'),
    path('^summary/',                              login_required(views.SummaryList.as_view()), name='summary_list'),
    path('^summary/filter/',                       views.summary_set_filter, name='summary_set_filter'),
    # path('^summary/(?P<y>\d+)/(?P<place>\w+)/$',    views.summary_detail, name='summary_detail'),
    # path('^summary/(?P<p>\d+)/(?P<y>\d+)/$',        views.summary_detail, name='summary_detail'),
)
