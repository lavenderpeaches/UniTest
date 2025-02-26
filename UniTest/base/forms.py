from django import forms
from .models import Test

class testForm(forms.ModelForm):
    class Meta:
        model = Test   
        fields = '__all__'  
        exclude = ['is_results_visible']
