from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from django.shortcuts import redirect

from .forms import ContactForm
from .models import Contact


class ContactView(View):
    def get(self, request):
        contact_form = ContactForm
        context = {
            'contact_form': contact_form
        }
        return render(request, 'contact_module/contact.html', context)

    def post(self, request):
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            user_full_name = contact_form.cleaned_data.get('full_name')
            user_phone = contact_form.cleaned_data.get('phone')
            user_message = contact_form.cleaned_data.get('message')
            new_ticket = Contact(
                full_name=user_full_name,
                phone=user_phone,
                message=user_message,
            )
            new_ticket.save()
            messages.success(request, 'پیام شما ثبت شد. با شما تماس گرفته خواهد شد.')
            return redirect('contact')
        context = {
            'contact_form': contact_form
        }
        return render(request, 'contact_module/contact.html', context)
