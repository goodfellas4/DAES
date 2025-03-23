from django import forms
from .models import Student

class StudentSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['registration_number', 'name', 'course', 'password']


class StudentLoginForm(forms.Form):
    registration_number = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)