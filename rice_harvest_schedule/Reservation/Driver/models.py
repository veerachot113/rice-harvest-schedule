#Driver/models.py
from django.db import models
from Accounts.models import UserDriver  

class Vehicle(models.Model):
    driver = models.OneToOneField(UserDriver, on_delete=models.CASCADE, related_name='vehicles')  # Add related_name='vehicles'
    model = models.CharField(max_length=100, verbose_name='รุ่น')
    TYPE_CHOICES = (
        ('แบบรองกระสอบ', 'แบบรองกระสอบ'),
        ('แบบถังอุ้ม', 'แบบถังอุ้ม'),
    )
    type = models.CharField(max_length=100,verbose_name='ประเภทรถ', choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='ราคา')
    PROVINCE_CHOICES = [
    ('กระบี่', 'กระบี่'),
    ('กรุงเทพมหานคร', 'กรุงเทพมหานคร'),
    ('กาญจนบุรี', 'กาญจนบุรี'),
    ('กาฬสินธุ์', 'กาฬสินธุ์'),
    ('กำแพงเพชร', 'กำแพงเพชร'),
    ('ขอนแก่น', 'ขอนแก่น'),
    ('จันทบุรี', 'จันทบุรี'),
    ('ฉะเชิงเทรา', 'ฉะเชิงเทรา'),
    ('ชลบุรี', 'ชลบุรี'),
    ('ชัยนาท', 'ชัยนาท'),
    ('ชัยภูมิ', 'ชัยภูมิ'),
    ('ชุมพร', 'ชุมพร'),
    ('เชียงราย', 'เชียงราย'),
    ('เชียงใหม่', 'เชียงใหม่'),
    ('ตรัง', 'ตรัง'),
    ('ตราด', 'ตราด'),
    ('ตาก', 'ตาก'),
    ('นครนายก', 'นครนายก'),
    ('นครปฐม', 'นครปฐม'),
    ('นครพนม', 'นครพนม'),
    ('นครราชสีมา', 'นครราชสีมา'),
    ('นครศรีธรรมราช', 'นครศรีธรรมราช'),
    ('นครสวรรค์', 'นครสวรรค์'),
    ('นนทบุรี', 'นนทบุรี'),
    ('นราธิวาส', 'นราธิวาส'),
    ('น่าน', 'น่าน'),
    ('บึงกาฬ', 'บึงกาฬ'),
    ('บุรีรัมย์', 'บุรีรัมย์'),
    ('ปทุมธานี', 'ปทุมธานี'),
    ('ประจวบคีรีขันธ์', 'ประจวบคีรีขันธ์'),
    ('ปราจีนบุรี', 'ปราจีนบุรี'),
    ('ปัตตานี', 'ปัตตานี'),
    ('พระนครศรีอยุธยา', 'พระนครศรีอยุธยา'),
    ('พะเยา', 'พะเยา'),
    ('พังงา', 'พังงา'),
    ('พัทลุง', 'พัทลุง'),
    ('พิจิตร', 'พิจิตร'),
    ('พิษณุโลก', 'พิษณุโลก'),
    ('เพชรบุรี', 'เพชรบุรี'),
    ('เพชรบูรณ์', 'เพชรบูรณ์'),
    ('แพร่', 'แพร่'),
    ('พะเยา', 'พะเยา'),
    ('ภูเก็ต', 'ภูเก็ต'),
    ('มหาสารคาม', 'มหาสารคาม'),
    ('มุกดาหาร', 'มุกดาหาร'),
    ('แม่ฮ่องสอน', 'แม่ฮ่องสอน'),
    ('ยโสธร', 'ยโสธร'),
    ('ยะลา', 'ยะลา'),
    ('ร้อยเอ็ด', 'ร้อยเอ็ด'),
    ('ระนอง', 'ระนอง'),
    ('ระยอง', 'ระยอง'),
    ('ราชบุรี', 'ราชบุรี'),
    ('ลพบุรี', 'ลพบุรี'),
    ('ลำปาง', 'ลำปาง'),
    ('ลำพูน', 'ลำพูน'),
    ('เลย', 'เลย'),
    ('ศรีสะเกษ', 'ศรีสะเกษ'),
    ('สกลนคร', 'สกลนคร'),
    ('สงขลา', 'สงขลา'),
    ('สตูล', 'สตูล'),
    ('สมุทรปราการ', 'สมุทรปราการ'),
    ('สมุทรสงคราม', 'สมุทรสงคราม'),
    ('สมุทรสาคร', 'สมุทรสาคร'),
    ('สระแก้ว', 'สระแก้ว'),
    ('สระบุรี', 'สระบุรี'),
    ('สิงห์บุรี', 'สิงห์บุรี'),
    ('สุโขทัย', 'สุโขทัย'),
    ('สุพรรณบุรี', 'สุพรรณบุรี'),
    ('สุราษฎร์ธานี', 'สุราษฎร์ธานี'),
    ('สุรินทร์', 'สุรินทร์'),
    ('หนองคาย', 'หนองคาย'),
    ('หนองบัวลำภู', 'หนองบัวลำภู'),
    ('อ่างทอง', 'อ่างทอง'),
    ('อำนาจเจริญ', 'อำนาจเจริญ'),
    ('อุดรธานี', 'อุดรธานี'),
    ('อุตรดิตถ์', 'อุตรดิตถ์'),
    ('อุทัยธานี', 'อุทัยธานี'),
    ('อุบลราชธานี', 'อุบลราชธานี'),
    ('อำนาจเจริญ', 'อำนาจเจริญ'),
]
    province = models.CharField(max_length=200, verbose_name='จังหวัดที่ลงพื้นที่',choices=PROVINCE_CHOICES)
    image = models.ImageField(upload_to='vehicle_images/',null=True, blank=True, verbose_name='รูปภาพรถ')


    def __str__(self):
        return self.model

#modelเพิ่มรายละเอียดรถ

class Detailvehicle(models.Model):
    driver = models.OneToOneField(UserDriver, on_delete=models.CASCADE, related_name='vehicles_detailvehicle')  # Add related_name='vehicles'
    power = models.CharField(max_length=100, verbose_name='กำลังเครื่อง')
    details = models.TextField(verbose_name='รายละเอียด')

    def __str__(self):
        return self.power


# Driver/models.py

from django.db import models
class CalendarEvent(models.Model):
    title = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    driver = models.ForeignKey(UserDriver, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
# Driver/models.py

from django.db import models
from Accounts.models import UserDriver

from django.db import models
from Accounts.models import UserDriver  

class LicenseDocument(models.Model):
    driver = models.ForeignKey(UserDriver, on_delete=models.CASCADE, related_name='license_documents')
    document = models.FileField(upload_to='license_documents/')
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    can_resubmit = models.BooleanField(default=True)  # เพิ่มฟิลด์เพื่อระบุว่าไฟล์สามารถส่งเอกสารใหม่ได้หรือไม่
    
    def __str__(self):
        return f"Document from {self.driver.username}"

    