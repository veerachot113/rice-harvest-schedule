# auth_admin/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import DriverDocument
from .forms import DriverDocumentForm
from accounts.models import CustomUser

@login_required
def upload_document(request):
    existing_document = DriverDocument.objects.filter(driver=request.user).exclude(request_status='Declined').first()
    if existing_document:
        messages.error(request, 'คุณได้ส่งเอกสารไปแล้ว รอการตรวจสอบหรือส่งใหม่ในกรณีที่ถูกปฏิเสธ')
        return redirect('document_status')

    if request.method == 'POST':
        form = DriverDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.driver = request.user
            document.save()
            messages.success(request, 'เอกสารถูกส่งเรียบร้อยแล้ว')
            return redirect('document_status')
    else:
        form = DriverDocumentForm()
    
    no_of_pending_documents = DriverDocument.objects.filter(driver=request.user, request_status="Pending").count()
    return render(request, 'driver/upload_document.html', {'form': form, 'no_of_pending_documents': no_of_pending_documents})

@login_required
def document_status(request):
    documents = DriverDocument.objects.filter(driver=request.user)
    no_of_pending_documents = DriverDocument.objects.filter(driver=request.user, request_status="Pending").count()
    return render(request, 'driver/document_status.html', {'documents': documents, 'no_of_pending_documents': no_of_pending_documents})

@user_passes_test(lambda u: u.is_superuser)
def document_review(request):
    documents = DriverDocument.objects.all()
    no_of_pending_documents = DriverDocument.objects.filter(request_status="Pending").count()
    return render(request, 'auth_admin/document_review.html', {'documents': documents, 'no_of_pending_documents': no_of_pending_documents})

@user_passes_test(lambda u: u.is_superuser)
def process_document(request, document_id):
    document = get_object_or_404(DriverDocument, id=document_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        note = request.POST.get('note', '')
        if action == 'approve':
            document.request_status = 'Approved'
            document.driver.is_staff = True
            document.driver.save()
        elif action == 'decline':
            document.request_status = 'Declined'
        else:
            messages.error(request, 'Invalid action.')
            return redirect('document_review')
        document.note = note
        document.save()
        messages.success(request, f'เอกสารได้ถูก{action}เรียบร้อยแล้ว')
    return redirect('document_review')


@user_passes_test(lambda u: u.is_superuser)
def user_list(request, user_type):
    no_of_pending_documents = DriverDocument.objects.filter(request_status="Pending").count()
    if user_type == 'farmer':
        users = CustomUser.objects.filter(user_type='farmer')
    elif user_type == 'driver':
        users = CustomUser.objects.filter(user_type='driver')
    else:
        messages.error(request, 'Invalid user type.')
        return redirect('home')
    
    return render(request, 'auth_admin/user_list.html', {'users': users, 'user_type': user_type,'no_of_pending_documents': no_of_pending_documents})

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, 'ผู้ใช้ได้ถูกลบเรียบร้อยแล้ว')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@user_passes_test(lambda u: u.is_superuser)
def view_driver_document(request, user_id):
    no_of_pending_documents = DriverDocument.objects.filter(request_status="Pending").count()
    driver = get_object_or_404(CustomUser, id=user_id, user_type='driver')
    documents = DriverDocument.objects.filter(driver=driver)
    return render(request, 'auth_admin/view_driver_document.html', {'driver': driver, 'documents': documents,'no_of_pending_documents': no_of_pending_documents})

@user_passes_test(lambda u: u.is_superuser)
def delete_document(request, document_id):
    document = get_object_or_404(DriverDocument, id=document_id)
    document.delete()
    messages.success(request, 'เอกสารได้ถูกลบเรียบร้อยแล้ว')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@user_passes_test(lambda u: u.is_superuser)
def delete_all_documents(request, user_id):
    driver = get_object_or_404(CustomUser, id=user_id, user_type='driver')
    documents = DriverDocument.objects.filter(driver=driver)
    documents.delete()
    messages.success(request, 'เอกสารทั้งหมดของผู้ใช้ได้ถูกลบเรียบร้อยแล้ว')
    return redirect('view_driver_document', user_id=user_id)
