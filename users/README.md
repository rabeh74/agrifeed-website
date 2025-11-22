# Users App - نظام المستخدمين

## 📖 نظرة عامة | Overview

تطبيق Django مخصص لإدارة المستخدمين مع تسجيل الدخول باستخدام البريد الإلكتروني.

A custom Django app for user management with email-based authentication.

## 🎯 الميزات الرئيسية | Key Features

- ✅ تسجيل الدخول بالبريد الإلكتروني (Email Authentication)
- ✅ نموذج مستخدم مخصص (Custom User Model)
- ✅ واجهات عربية متجاوبة (Arabic Responsive UI)
- ✅ إدارة متقدمة في Admin Panel
- ✅ أمان عالي (High Security)

## 📁 هيكل الملفات | File Structure

```
users/
├── models.py           # CustomUser model with email as username
├── backends.py         # Email authentication backend
├── forms.py            # Registration, login, and profile forms
├── views.py            # Login, register, logout, profile views
├── urls.py             # URL patterns
├── admin.py            # Custom admin interface
├── apps.py             # App configuration
└── templates/users/
    ├── login.html      # Login page
    ├── register.html   # Registration page
    └── profile.html    # User profile page
```

## 🔗 المسارات | URL Patterns

```python
/users/login/      # تسجيل الدخول
/users/register/   # إنشاء حساب جديد
/users/logout/     # تسجيل الخروج
/users/profile/    # الملف الشخصي
```

## 💻 أمثلة الاستخدام | Usage Examples

### في Views
```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    user = request.user
    print(user.email)
    print(user.get_full_name())
```

### في Templates
```django
{% if user.is_authenticated %}
    مرحباً {{ user.get_full_name }}
{% endif %}
```

## 🔧 الإعداد | Setup

راجع: `../SETUP_USERS_APP.md`
See: `../SETUP_USERS_APP.md`

## 📚 التوثيق الكامل | Full Documentation

راجع: `../USERS_APP_README.md`
See: `../USERS_APP_README.md`

## 🚀 البدء السريع | Quick Start

```bash
# 1. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 2. Create superuser
python create_email_superuser.py

# 3. Run server
python manage.py runserver

# 4. Visit
# http://localhost:8000/users/login/
```

---

Made with ❤️ for Agree Feed

