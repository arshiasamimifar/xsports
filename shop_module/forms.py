from django import forms
from .models import ProductComment


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['body']
        labels = {
            'body': 'نظر شما',
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-clt',
                'placeholder': 'متن پیام خودت رو بنویس ...'
            })
        }
