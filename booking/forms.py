from django import forms

class YourForm(forms.Form):
    your_field = forms.CharField(label='Your label', max_length=100)
    # 他のフィールドをここに追加します