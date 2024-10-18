# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordResetForm,SetPasswordForm,PasswordChangeForm
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, required=True)

    def get_users(self, email):
        active_users = CustomUser._default_manager.filter(
            email__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='รหัสผ่านใหม่', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='ยืนยันรหัสผ่านใหม่', widget=forms.PasswordInput)

class UserFarmerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label='ชื่อ',error_messages={'required': 'กรุณากรอกชื่อ'})
    last_name = forms.CharField(max_length=100, required=True, label='นามสกุล',error_messages={'required': 'กรุณากรอกนามสกุล'})
    address = forms.CharField(max_length=255, required=True, label='ที่อยู่',error_messages={'required': 'กรุณากรอกที่อยู่'})
    phone = forms.CharField(max_length=15, required=True, label='เบอร์',error_messages={'required': 'กรุณากรอกเบอร์โทรศัพท์'})
    email = forms.EmailField(required=True, label='E-mail',error_messages={    'required': 'กรุณากรอกอีเมล',    'invalid': 'รูปแบบอีเมลไม่ถูกต้อง'})
    username = forms.CharField(max_length=150, required=True, label='Username',error_messages={    'required': 'กรุณากรอกชื่อผู้ใช้',    'unique': 'ชื่อผู้ใช้นี้มีอยู่แล้ว'})
    password1 = forms.CharField(label='รหัสผ่าน', widget=forms.PasswordInput,error_messages={    'required': 'กรุณากรอกรหัสผ่าน',})
    password2 = forms.CharField(label='ยืนยันรหัสผ่าน', widget=forms.PasswordInput,error_messages={    'required': 'กรุณากรอกยืนยันรหัสผ่าน',    'password_mismatch': 'รหัสผ่านไม่ตรงกัน'})

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'address', 'phone']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('อีเมลนี้มีอยู่แล้วในระบบ')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('ชื่อผู้ใช้นี้มีอยู่แล้วในระบบ')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('รหัสผ่านไม่ตรงกัน')
        return password2
class UserDriverRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label='ชื่อ',error_messages={'required': 'กรุณากรอกชื่อ'})
    last_name = forms.CharField(max_length=100, required=True, label='นามสกุล',error_messages={'required': 'กรุณากรอกนามสกุล'})
    address = forms.CharField(max_length=255, required=True, label='ที่อยู่',error_messages={'required': 'กรุณากรอกที่อยู่'})
    phone = forms.CharField(max_length=15, required=True, label='เบอร์',error_messages={'required': 'กรุณากรอกเบอร์โทรศัพท์'})
    email = forms.EmailField(required=True, label='E-mail',error_messages={'required': 'กรุณากรอกอีเมล','invalid': 'รูปแบบอีเมลไม่ถูกต้อง'})
    username = forms.CharField(max_length=150, required=True, label='Username',error_messages={'required': 'กรุณากรอกชื่อผู้ใช้','unique': 'ชื่อผู้ใช้นี้มีอยู่แล้ว'})
    password1 = forms.CharField(label='รหัสผ่าน', widget=forms.PasswordInput,error_messages={'required': 'กรุณากรอกรหัสผ่าน',})
    password2 = forms.CharField(label='ยืนยันรหัสผ่าน', widget=forms.PasswordInput,error_messages={'required': 'กรุณากรอกยืนยันรหัสผ่าน','password_mismatch': 'รหัสผ่านไม่ตรงกัน'})

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'address', 'phone']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('อีเมลนี้มีอยู่แล้วในระบบ')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('ชื่อผู้ใช้นี้มีอยู่แล้วในระบบ')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('รหัสผ่านไม่ตรงกัน')
        return password2

class UserFarmerUpdateForm(UserChangeForm):
    first_name = forms.CharField(max_length=100, required=True, label='ชื่อ')
    last_name = forms.CharField(max_length=100, required=True, label='นามสกุล')
    address = forms.CharField(max_length=255, required=True, label='ที่อยู่')
    phone = forms.CharField(max_length=15, required=True, label='เบอร์โทรศัพท์')

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'address', 'phone']

class UserDriverUpdateForm(UserChangeForm):
    first_name = forms.CharField(max_length=100, required=True, label='ชื่อ')
    last_name = forms.CharField(max_length=100, required=True, label='นามสกุล')
    address = forms.CharField(max_length=255, required=True, label='ที่อยู่')
    phone = forms.CharField(max_length=15, required=True, label='เบอร์โทรศัพท์')

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'address', 'phone']

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="รหัสผ่านเดิม", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label="รหัสผ่านใหม่", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label="ยืนยันรหัสผ่านใหม่", widget=forms.PasswordInput(attrs={'class': 'form-control'}))



