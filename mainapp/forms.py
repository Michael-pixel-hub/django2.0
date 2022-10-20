from django.contrib.auth.forms import forms
from mainapp.models import CourseFeedback
from django.urls import reverse_lazy as _


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, course=None, user=None, **kwargs):
        ret = super().__init__(*args, **kwargs)
        if course and user:
            self.fields["course"].initial = course.pk
            self.fields["user"].initial = user.pk
        return ret

    class Meta:
        model = CourseFeedback
        fields = ('course', 'user', 'rating', 'feedback')
        widgets = {
            'course': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'rating': forms.RadioSelect()
        }


class MailFeedbackForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput)
    message = forms.CharField(
        widget=forms.Textarea,
        help_text="Enter your message",
        label=_("Message"),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["user_id"].initial = user.pk
