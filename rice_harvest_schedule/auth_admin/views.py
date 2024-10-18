# auth_admin/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import DriverDocument
from .forms import DriverDocumentForm
from accounts.models import CustomUser
from bookings.models import Booking
from django.utils import timezone
from accounts.decorators import*


@login_required
@driver_required
def upload_document(request):
    no_of_pending_request = Booking.objects.filter(vehicle__driver=request.user, request_status="รอดำเนินการ").count()
    no_of_pending_documents = DriverDocument.objects.filter(driver=request.user, request_status="รอดำเนินการ").count()
    existing_document = DriverDocument.objects.filter(driver=request.user).exclude(request_status__in=['ปฏิเสธ', 'ยกเลิกแล้ว']).first()
    if existing_document:
        messages.error(request, 'คุณได้ส่งเอกสารไปแล้ว รอการตรวจสอบหรือส่งใหม่ในกรณีที่ถูกปฏิเสธหรือยกเลิก')
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
    return render(request, 'driver/upload_document.html', {'form': form, 'no_of_pending_documents': no_of_pending_documents, 'no_of_pending_request': no_of_pending_request})

@login_required
@driver_required
def cancel_document(request, document_id):
    document = get_object_or_404(DriverDocument, id=document_id, driver=request.user)
    if document.request_status == 'รอดำเนินการ':
        document.request_status = 'ยกเลิกแล้ว'
        document.save()
        messages.success(request, 'เอกสารถูกยกเลิกเรียบร้อยแล้ว')
    else:
        messages.error(request, 'ไม่สามารถยกเลิกเอกสารที่ได้รับการอนุมัติหรือถูกปฏิเสธแล้ว')
    return redirect('document_status')

@login_required
@driver_required
def document_status(request):
    documents = DriverDocument.objects.filter(driver=request.user)
    no_of_pending_documents = DriverDocument.objects.filter(driver=request.user, request_status="รอดำเนินการ").count()
    no_of_pending_request = Booking.objects.filter(vehicle__driver=request.user, request_status="รอดำเนินการ").count()
    return render(request, 'driver/document_status.html', {'documents': documents, 'no_of_pending_documents': no_of_pending_documents, 'no_of_pending_request': no_of_pending_request})

@user_passes_test(lambda u: u.is_superuser)
def document_review(request):
    documents = DriverDocument.objects.all()
    no_of_pending_documents = DriverDocument.objects.filter(request_status="รอดำเนินการ").count()
    return render(request, 'auth_admin/document_review.html', {'documents': documents, 'no_of_pending_documents': no_of_pending_documents})

@user_passes_test(lambda u: u.is_superuser)
def process_document(request, document_id):
    document = get_object_or_404(DriverDocument, id=document_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        note = request.POST.get('note', '')
        if action == 'approve':
            document.request_status = 'อนุมัติแล้ว'
            document.driver.is_staff = True
            document.driver.is_active = True
            document.driver.save()
        elif action == 'decline':
            document.request_status = 'ปฏิเสธ'
        else:
            messages.error(request, 'Invalid action.')
            return redirect('document_review')
        document.note = note
        document.response_date = timezone.now()  
        document.save()
        messages.success(request, f'เอกสารได้ถูก{action}เรียบร้อยแล้ว')
    return redirect('document_review')

@user_passes_test(lambda u: u.is_superuser)
def delete_all_documents(request, user_id):
    driver = get_object_or_404(CustomUser, id=user_id, user_type='driver')
    documents = DriverDocument.objects.filter(driver=driver)
    if request.method == 'POST':
        documents.delete() 
        driver.is_staff = False
        driver.is_active = False 
        driver.save()
        messages.success(request, 'เอกสารทั้งหมดของผู้ใช้ได้ถูกลบเรียบร้อยแล้ว และสถานะผู้ใช้ถูกเปลี่ยนเป็นไม่ทำงานแล้ว')
    return redirect('view_driver_document', user_id=user_id)


@user_passes_test(lambda u: u.is_superuser)
def user_list(request, user_type):
    no_of_pending_documents = DriverDocument.objects.filter(request_status="รอดำเนินการ").count()

    if user_type == 'farmer':
        users = CustomUser.objects.filter(user_type='farmer')
        user_type_name = 'ชาวนา'
    elif user_type == 'driver':
        users = CustomUser.objects.filter(user_type='driver')
        user_type_name = 'คนขับรถเกี่ยว'
    else:
        messages.error(request, 'Invalid user type.')
        return redirect('home')
    
    return render(request, 'auth_admin/user_list.html', {
        'users': users, 
        'user_type': user_type, 
        'user_type_name': user_type_name,
        'no_of_pending_documents': no_of_pending_documents
    })


@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, 'ผู้ใช้ได้ถูกลบเรียบร้อยแล้ว')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@user_passes_test(lambda u: u.is_superuser)
def view_driver_document(request, user_id):
    no_of_pending_documents = DriverDocument.objects.filter(request_status="รอดำเนินการ").count()
    driver = get_object_or_404(CustomUser, id=user_id, user_type='driver')
    documents = DriverDocument.objects.filter(driver=driver, request_status='อนุมัติแล้ว')
    return render(request, 'auth_admin/view_driver_document.html', {'driver': driver, 'documents': documents, 'no_of_pending_documents': no_of_pending_documents})
