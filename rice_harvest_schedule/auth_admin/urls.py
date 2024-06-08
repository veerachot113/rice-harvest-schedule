from django.urls import path
from .views import *

urlpatterns = [
    path('document-list/', document_list, name='document_list'),
    path('upload-document/', upload_document, name='upload_document'),
    path('approve-document/<int:document_id>/', approve_document, name='approve_document'),
    path('reject-document/<int:document_id>/', reject_document, name='reject_document'),
    path('document-status/', document_status, name='document_status'),

]
