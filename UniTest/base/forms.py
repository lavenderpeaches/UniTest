from django import forms
from .models import Test

class TestForm(forms.ModelForm):
    class Meta:
        model = Test   
        exclude = ['is_results_visible']
