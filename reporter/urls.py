from django.urls import path
from . import views

app_name = 'reporter'

urlpatterns=[
    path('',views.index_view,name='index'),
    path('report/',views.issue_form_view,name='issue-form'),
    path('archived/',views.archive_view,name='archived'),
    path('close/<int:pk>',views.close_issue_view,name='close'),
]