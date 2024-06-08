from django.db import models
from accounts.models import UserDriver

class LicenseDocument(models.Model):
    driver = models.ForeignKey(UserDriver, on_delete=models.CASCADE, related_name='license_documents')
    id_card = models.FileField(upload_to='license_documents/id_card/')
    driving_license = models.FileField(upload_to='license_documents/driving_license/')
    vehicle_registration = models.FileField(upload_to='license_documents/vehicle_registration/')
    photo = models.ImageField(upload_to='license_documents/photo/', default='')
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    reason = models.TextField(blank=True, null=True ,default='')  # เปลี่ยนจาก rejection_reason เป็น reason
    submitted_at = models.DateTimeField(auto_now_add=True)
    can_resubmit = models.BooleanField(default=True)

    def __str__(self):
        return f"Document from {self.driver.username}"

