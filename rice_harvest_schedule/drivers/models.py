#dirvers/models.py
from datetime import datetime
from django.db import models
from accounts.models import CustomUser
from django.conf import settings

class Vehicle(models.Model):
    driver = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='vehicles', limit_choices_to={'user_type': 'driver'})
    model = models.CharField(max_length=100, verbose_name='รุ่น')
    TYPE_CHOICES = (
        ('แบบรองกระสอบ', 'แบบรองกระสอบ'),
        ('แบบถังอุ้ม', 'แบบถังอุ้ม'),
    )
    type = models.CharField(max_length=100,verbose_name='ประเภทรถ', choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='ราคา (ไร่)')
    
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
    min_acres = models.IntegerField(default='', verbose_name='ขั้นต่ำที่รับเกี่ยว (ไร่)')
    max_acres_per_day = models.IntegerField(default='', verbose_name='จำนวนไร่สูงสุดที่เกี่ยวได้ต่อวัน (ไร่)')
    status = models.BooleanField(default=True, verbose_name='สถานะการให้บริการ')


    def __str__(self):
        return self.model

class CalendarEvent(models.Model):
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    details = models.TextField(blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    farmer = models.ForeignKey(CustomUser, on_delete=models.CASCADE ,related_name='events', null=True)
    google_event_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

class HarvestArea(models.Model):
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()   # Added end_date field
    province = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    subdistrict = models.CharField(max_length=100)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.province} - {self.district} - {self.subdistrict}'

class VehicleDetail(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='details')
    power = models.CharField(max_length=100, verbose_name='กำลังเครื่อง')
    image1 = models.ImageField(upload_to='vehicle_detail_images/', null=True, blank=True, verbose_name='รูปภาพ 1')
    image2 = models.ImageField(upload_to='vehicle_detail_images/', null=True, blank=True, verbose_name='รูปภาพ 2')
    image3 = models.ImageField(upload_to='vehicle_detail_images/', null=True, blank=True, verbose_name='รูปภาพ 3')
    details = models.TextField(verbose_name='รายละเอียดรถ', default='')

    def __str__(self):
        return f"{self.vehicle.model} - Details"
