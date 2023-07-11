from datetime import timedelta
from django.utils import timezone
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_from_email(self):
        data = self.cleaned_data["from_email"]

        if data.strip().endswith("mail.ru"):
            raise ValidationError(_("We can't send email on mail.ru emails"))

        return data

    def clean(self):
        email = self.cleaned_data["from_email"]
        subject = self.cleaned_data["subject"]

        if email.endswith("gmail.com") and "spam" in subject.lower():
            self.add_error(None, "Can't send spam emails")


class ReminderForm(forms.Form):
    to_email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    when = forms.DateTimeField()

    def clean_when(self):
        now = timezone.now()
        when = self.cleaned_data.get("when")
        if when < now:
            raise ValidationError("You cant select date less than now, blit")
        if when > now + timedelta(days=2):
            raise ValidationError("You cant chose date more than 2 days")
        return when
