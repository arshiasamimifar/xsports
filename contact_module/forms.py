from django import forms
from django.core.validators import RegexValidator


class ContactForm(forms.Form):
    full_name = forms.CharField(
        label='نام و نام خانوادگی',
        min_length=6,
        max_length=72,
        widget=forms.TextInput(attrs={
            'class': 'form-clt',
            'placeholder': 'نام شما'
        }),
    )

    phone = forms.CharField(
        label='تلفن همراه',
        min_length=11,
        max_length=11,
        widget=forms.TextInput(attrs={
            'class': 'form-clt',
            'placeholder': 'تلفن همراه شما',
        }),
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message='تلفن همراه خود را درست وارد کنید!'
            )
        ],
    )

    message = forms.CharField(
        label='پیام شما',
        widget=forms.Textarea(attrs={
            'class': 'col-lg-12',
            'placeholder': 'پیام شما',
            'rows': '5',
        }),
    )
