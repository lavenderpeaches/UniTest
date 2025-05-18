from django  import forms
from .models import Test, Batch, Course, Question, Choice, Student


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

class StudentImportForm(forms.Form):
    csv_file = forms.FileField(
        label='Select CSV file',
        help_text='CSV file should have columns: Name, Email, Roll Number'
    )
    
    def clean_csv_file(self):
        file = self.cleaned_data['csv_file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('File must be a CSV file')
        return file
