"""
core.urls
"""

from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = (
    path('f/',                 login_required(views.FileList.as_view()), name='file_list'),
    path('f/<int:pk>/',        login_required(views.FileDetail.as_view()), name='file_view'),
    path('f/<int:pk>/g/',      views.file_get, name='file_get'),
    path('f/<int:pk>/d/',      views.file_del, name='file_del'),
    path('f/<int:pk>/v/',      views.file_preview, name='file_preview'),
    path('fs/',                login_required(views.FileSeqList.as_view()), name='fileseq_list'),
    path('fs/<int:pk>/',       login_required(views.FileSeqDetail.as_view()), name='fileseq_view'),
    path('fs/<int:pk>/d/',     views.fileseq_del, name='fileseq_del'),
    path('fs/<int:pk>/af/',    views.fileseq_add_file, name='fileseq_add_file'),
    path('fsi/<int:pk>/d/',    views.fileseqitem_del, name='fileseqitem_del'),
    path('fsi/<int:pk>/up/',   views.fileseqitem_move_up, name='fileseqitem_move_up'),
    path('fsi/<int:pk>/down/', views.fileseqitem_move_down, name='fileseqitem_move_down'),
)
