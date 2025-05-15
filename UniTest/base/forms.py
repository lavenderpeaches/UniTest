from django  import forms
from .models import Test, Batch, Course, Question, Choice


class testForm(forms.ModelForm):
    class Meta:
        model = Test
        exclude = ['user', 'status', 'is_results_visible','total_questions', 'total_marks']

class batchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = '__all__'

class courseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
