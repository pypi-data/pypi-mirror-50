from django import forms
from feedback.tasks import send_feedback_email_task


class FeedbackForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    message = forms.CharField(
        label="Message", widget=forms.Textarea(attrs={'rows': 5}))
    honeypot = forms.CharField(widget=forms.HiddenInput(), required=False)

    def send_email(self):
        # interesting way to check for spambots
        if self.cleaned_data['honeypot']:
            return False
        # the below function processes and sends the feedback
        # email in the background as the user continues to use the site.
        send_feedback_email_task.delay(
            self.cleaned_data['email'], self.cleaned_data['message'])
