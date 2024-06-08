from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .forms import LicenseDocumentForm, ReviewDocumentForm
from .models import LicenseDocument
from accounts.models import UserDriver

User = get_user_model()

@login_required
@user_passes_test(lambda u: u.is_superuser)
def document_list(request):
    pending_documents = LicenseDocument.objects.filter(is_approved=False, is_rejected=False)
    approved_documents = LicenseDocument.objects.filter(is_approved=True)
    rejected_documents = LicenseDocument.objects.filter(is_rejected=True)
    return render(request, 'auth_admin/document_list.html', {
        'pending_documents': pending_documents,
        'approved_documents': approved_documents,
        'rejected_documents': rejected_documents,
    })

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = LicenseDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            driver = request.user
            if LicenseDocument.objects.filter(driver=driver, is_approved=False, is_rejected=False).exists():
                form.add_error(None, "You have already submitted a document for approval.")
            else:
                form.instance.driver = driver
                form.save()
                return redirect('document_status')
    else:
        form = LicenseDocumentForm()
    return render(request, 'Driver/upload_document.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def approve_document(request, document_id):
    document = get_object_or_404(LicenseDocument, id=document_id)
    if request.method == 'POST':
        document.is_approved = True
        document.save()
        document.driver.is_staff = True
        document.driver.save()
        return redirect('document_list')
    return render(request, 'auth_admin/review_document.html', {'document': document})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def reject_document(request, document_id):
    document = get_object_or_404(LicenseDocument, id=document_id)
    if request.method == 'POST':
        form = ReviewDocumentForm(request.POST, instance=document)
        if form.is_valid():
            document.is_rejected = True
            document.can_resubmit = True
            document.save()
            return redirect('document_list')
    else:
        form = ReviewDocumentForm(instance=document)
    return render(request, 'auth_admin/review_document.html', {'form': form, 'document': document})

@login_required
def document_status(request):
    documents = LicenseDocument.objects.filter(driver=request.user)
    return render(request, 'Driver/document_status.html', {'documents': documents})
