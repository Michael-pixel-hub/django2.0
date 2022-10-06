from django.contrib.auth.forms import forms
from mainapp.models import CourseFeedback


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
