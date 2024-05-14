from django import forms
from .models import Staff

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'  # すべてのフィールドをフォームに含める

class YourForm(forms.Form):
    your_field = forms.CharField(label='Your label', max_length=100)

