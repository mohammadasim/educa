from django import forms
from courses.models import Course


class CourseEnrollForm(forms.Form):
    """
    Form for a student to enroll on a course.
    Course field is set to hidden as user will not see this field.
    A button in course_detail page will allow a student to enroll
    on a course.
    """
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput())
