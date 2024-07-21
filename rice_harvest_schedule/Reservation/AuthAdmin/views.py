# AuthAdmin/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Driver.models import LicenseDocument

@login_required
def admin_document_list(request):
    documents = LicenseDocument.objects.filter(is_approved=False, is_rejected=False)
    return render(request, 'authadmin/document_list.html', {'documents': documents})

@login_required
def admin_approve_document(request, document_id):
    document = get_object_or_404(LicenseDocument, id=document_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            document.is_approved = True
            document.is_rejected = False
        elif action == 'reject':
            document.is_approved = False
            document.is_rejected = True
        document.save()
        return redirect('admin_document_list')
    return render(request, 'authadmin/approve_document.html', {'document': document})
