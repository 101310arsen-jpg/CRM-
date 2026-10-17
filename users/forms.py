from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Student

FIELDS = (
    'username', 'last_name', 'first_name', 'middle_name', 'email', 'birth_date',
    'gender', 'phone', 'address', 'photo', 'student_id', 'group', 'specialty',
    'course', 'admission_year', 'education_form', 'funding', 'status',
)


class StudentCreateForm(UserCreationForm):
    class Meta:
        model = Student
        fields = FIELDS
        widgets = {'birth_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = FIELDS
        widgets = {'birth_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}