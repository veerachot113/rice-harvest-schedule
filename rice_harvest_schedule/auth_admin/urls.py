# auth_admin/urls.py
from django.urls import path
from .views import *
urlpatterns = [
    path('upload_document/', upload_document, name='upload_document'),
    path('document_status/', document_status, name='document_status'),
    path('document_review/', document_review, name='document_review'),
    path('process_document/<int:document_id>/', process_document, name='process_document'),
    path('user_list/<str:user_type>/', user_list, name='user_list'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('view_driver_document/<int:user_id>/', view_driver_document, name='view_driver_document'),
    path('delete_document/<int:document_id>/', delete_document, name='delete_document'),
    path('delete_all_documents/<int:user_id>/', delete_all_documents, name='delete_all_documents'),
    path('cancel_document/<int:document_id>/', cancel_document, name='cancel_document'),
]