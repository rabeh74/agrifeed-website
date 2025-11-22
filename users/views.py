from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import UserLoginForm, UserUpdateForm


def login_view(request):
    """View for user login"""
    if request.user.is_authenticated:
        return redirect('store:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'مرحباً {user.get_full_name()}!')
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('store:dashboard')
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})


@require_http_methods(["POST"])
def logout_view(request):
    """View for user logout"""
    logout(request)
    messages.info(request, 'تم تسجيل الخروج بنجاح')
    return redirect('users:login')


@login_required
def profile_view(request):
    """View for user profile"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الملف الشخصي بنجاح!')
            return redirect('users:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})

