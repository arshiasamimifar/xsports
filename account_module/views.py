from django.contrib.auth import login, logout
from django.views.generic import View
from .forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm
from django.shortcuts import render, redirect
from account_module.models import CustomUser
from django.utils.crypto import get_random_string
from django.contrib import messages
from utils.email_service import send_email


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user: CustomUser = CustomUser.objects.filter(email__iexact=user_email).first()
            if user is None:
                login_form.add_error('email', 'ایمیل یا کلمه عبور اشتباه است')
            elif not user.is_active:
                login_form.add_error('email', 'حساب شما فعال نشده است، ایمیل خود را بررسی کنید.')
            elif not user.check_password(user_password):
                login_form.add_error('email', 'ایمیل یا کلمه عبور اشتباه است')
            else:
                login(request, user)
                return redirect('home')
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user = CustomUser.objects.filter(email__iexact=user_email).first()
            if user:
                if user.is_active:
                    register_form.add_error('email', 'با این ایمیل قبلا ثبت نام شده است!')
                else:
                    register_form.add_error('email',
                                            'حساب شما از قبل ایجاد شده! برای فعالسازی ایمیل خود را بررسی کنید!')
            else:
                new_user = CustomUser(
                    email=user_email,
                    username=user_email,
                    is_active=False,
                    email_active_code=get_random_string(128)
                )
                new_user.set_password(user_password)
                new_user.save()
                send_email(
                    'فعالسازی حساب کاربری',
                    new_user.email,
                    {'user': new_user},
                    'emails/activate_account.html',
                )
                messages.success(request, 'حساب شما ایجاد شد، برای فعالسازی ایمیل خود را بررسی کنید')
                return redirect('login')
        context = {'register_form': register_form}
        return render(request, 'account_module/register.html', context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: CustomUser = CustomUser.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                messages.success(request, 'حساب کاربری شما فعال شد! فقط کافیست وارد شوید!')
                return redirect('login')
            else:
                messages.success(request, 'حساب کاربری شما فعال شد! فقط کافیست وارد شوید!')
                return redirect('login')
        messages.error(request, 'ایمیلی یافت نشد، لطفا ثبت نام کنید!')
        return redirect('login')


class ForgotPasswordView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('login')
        forgot_password_form = ForgotPasswordForm()
        context = {
            'forgot_password_form': forgot_password_form
        }
        return render(request, 'account_module/forgot_password.html', context)

    def post(self, request):
        forgot_password_form = ForgotPasswordForm(request.POST)
        if forgot_password_form.is_valid():
            user_email = forgot_password_form.cleaned_data.get('email')
            user: CustomUser = CustomUser.objects.filter(email__iexact=user_email).first()
            if not user:
                messages.success(request,
                                 'در صورتی که حسابی با این ایمیل وجود داشته باشد، لینک بازیابی رمز عبور برایتان ارسال می‌شود.')
                return redirect('login')
            else:
                send_email(
                    'بازیابی کلمه عبور',
                    user.email,
                    {'user': user},
                    'emails/forgot_password.html',
                )
                messages.success(request,
                                 'در صورتی که حسابی با این ایمیل وجود داشته باشد، لینک بازیابی رمز عبور برایتان ارسال می‌شود.')
                return redirect('login')
        context = {
            'forgot_password_form': forgot_password_form
        }
        return render(request, 'account_module/forgot_password.html', context)


class ResetPasswordView(View):
    def get(self, request, email_active_code):
        user: CustomUser = CustomUser.objects.filter(email_active_code__iexact=email_active_code)
        if not user:
            messages.error(request,
                           'لینک بازیابی رمز عبور نامعتبر یا منقضی شده است. لطفاً مجدداً درخواست بازیابی رمز عبور ارسال کنید.')
            return redirect('forgot_password')
        reset_password_form = ResetPasswordForm()
        context = {
            'reset_password_form': reset_password_form
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request, email_active_code):
        reset_password_form = ResetPasswordForm(request.POST)
        user: CustomUser = CustomUser.objects.filter(email_active_code__iexact=email_active_code).first()
        if reset_password_form.is_valid():
            user = CustomUser.objects.filter(email_active_code__iexact=email_active_code).first()
            if user is None:
                messages.error(request,
                               'لینک بازیابی رمز عبور نامعتبر یا منقضی شده است. لطفاً مجدداً درخواست بازیابی رمز عبور ارسال کنید.')
                return redirect('forgot_password')
            user_password = reset_password_form.cleaned_data.get('password')
            user.set_password(user_password)
            user.email_active_code = get_random_string(128)
            user.is_active = True
            user.save()
            messages.success(request, 'کلمه عبور شما با موفقیت تغییر کرد.')
            return redirect('login')
        context = {
            'reset_password_form': reset_password_form,
            'user': user,
        }
        return render(request, 'account_module/reset_password.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'شما از حساب کاربری خارج شدید.')
        return redirect('login')
