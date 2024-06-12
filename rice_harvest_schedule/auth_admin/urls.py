from django.urls import path
from .views import *
urlpatterns = [
    path('upload_document/', upload_document, name='upload_document'),
    path('document_status/', document_status, name='document_status'),
    path('document_review/', document_review, name='document_review'),
    path('process_document/<int:document_id>/', process_document, name='process_document'),
]