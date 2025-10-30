from django import forms
from django.core.validators import RegexValidator


class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        label='نام',
        min_length=3,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام خود را وارد کنید',
        }),
    )

    last_name = forms.CharField(
        label='نام خانوادگی',
        min_length=3,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام خانوادگی خود را وارد کنید',
        }),
    )
    email = forms.EmailField(
        label='ایمیل',
        min_length=6,
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'input100',
            'placeholder': 'ایمیل خود را وارد کنید',
        })
    )
    phone = forms.CharField(
        label='شماره تلفن',
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message='شماره تلفن باید با 09 شروع شود و دقیقا 11 رقم باشد.'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'input100',
            'placeholder': 'شماره تلفن خود را وارد کنید'
        })
    )

    address = forms.CharField(
        label='آدرس',
        min_length=15,
        max_length=300,
        widget=forms.Textarea(attrs={
            'class': 'input100',
            'placeholder': 'آدرس خود را وارد کنید'
        })
    )
