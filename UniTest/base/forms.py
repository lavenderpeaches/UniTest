from django  import forms
from .models import Test, Batch, Course, Question, Choice, Student
from datetime import timedelta


class testForm(forms.ModelForm):
    duration_minutes = forms.IntegerField(label='Duration (minutes)', min_value=1, required=True)

    class Meta:
        model = Test
        fields = ['name', 'course', 'batch', 'total_marks', 'total_questions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.duration:
            self.fields['duration_minutes'].initial = int(self.instance.duration.total_seconds() // 60)

    def save(self, commit=True):
        instance = super().save(commit=False)
        minutes = self.cleaned_data.get('duration_minutes', 1)
        instance.duration = timedelta(minutes=minutes)
        if commit:
            instance.save()
        return instance

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
