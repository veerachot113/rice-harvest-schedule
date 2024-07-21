# AuthAdmin/urls.py

from django.urls import path
from .views import admin_document_list, admin_approve_document

urlpatterns = [
    path('documents/', admin_document_list, name='admin_document_list'),
    path('documents/<int:document_id>/', admin_approve_document, name='admin_approve_document'),
]
