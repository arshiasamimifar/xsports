from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        min_length=6,
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'input100',
            'placeholder': 'ایمیل خود را وارد کنید',
            'autocomplete': 'new-password',
        })
    )
    password = forms.CharField(
        label='کلمه عبور',
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'input100',
            'placeholder': 'کلمه عبور خود را وارد کنید',
            'autocomplete': 'new-password',
        })
    )


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        min_length=6,
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'input100',
            'placeholder': 'ایمیل خود را وارد کنید',
        })
    )

    password = forms.CharField(
        label='کلمه عبور',
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'input100',
            'placeholder': 'کلمه عبور خود را وارد کنید',
            'autocomplete': 'new-password',
        })
    )

    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'input100',
            'placeholder': 'کلمه عبور خود را تکرار کنید',
            'autocomplete': 'new-password',
        })
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        else:
            raise ValidationError('تکرار کلمه عبور اشتباه است.')


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        min_length=6,
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'input100',
            'placeholder': 'ایمیل خود را وارد کنید',
        })
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='کلمه عبور',
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'input100',
            'placeholder': 'کلمه عبور خود را وارد کنید',
            'autocomplete': 'new-password',
        })
    )

    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'input100',
            'placeholder': 'کلمه عبور خود را تکرار کنید',
            'autocomplete': 'new-password',
        })
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return password
        else:
            raise ValidationError('تکرار کلمه عبور اشتباه است.')