from django import forms
from .models import ArticleComment


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
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
