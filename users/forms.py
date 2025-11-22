from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser


class UserRegistrationForm(BaseUserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(
        label='البريد الإلكتروني',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل البريد الإلكتروني'
        })
    )
    first_name = forms.CharField(
        label='الاسم الأول',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل الاسم الأول'
        })
    )
    last_name = forms.CharField(
        label='اسم العائلة',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل اسم العائلة'
        })
    )
    phone_number = forms.CharField(
        label='رقم الهاتف',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل رقم الهاتف (اختياري)'
        })
    )
    password1 = forms.CharField(
        label='كلمة المرور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل كلمة المرور'
        })
    )
    password2 = forms.CharField(
        label='تأكيد كلمة المرور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'أعد إدخال كلمة المرور'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('هذا البريد الإلكتروني مسجل بالفعل')
        return email


class UserLoginForm(AuthenticationForm):
    """Form for user login"""
    username = forms.EmailField(
        label='البريد الإلكتروني',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل البريد الإلكتروني',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='كلمة المرور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل كلمة المرور'
        })
    )


class UserUpdateForm(forms.ModelForm):
    """Form for updating user profile"""
    email = forms.EmailField(
        label='البريد الإلكتروني',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )
    first_name = forms.CharField(
        label='الاسم الأول',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(
        label='اسم العائلة',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    phone_number = forms.CharField(
        label='رقم الهاتف',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number')

