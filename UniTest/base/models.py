from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Batch(models.Model):
    batch_name    = models.CharField(max_length=255)
    batch_section = models.CharField(max_length=3)
    batch_session = models.CharField(max_length=20)
    semester      = models.IntegerField()

    def __str__(self):
        return f"{self.batch_name} | {self.batch_session} | {self.semester}th sem | {self.batch_section}"

class Student(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    roll_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

class Course(models.Model):
    course_name = models.CharField(max_length=255, unique=True)
    course_code = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.course_name} | {self.course_code}"

class Test(models.Model):
    name               = models.CharField(max_length=255)
    course             = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, default=None)
    batch              = models.ForeignKey(Batch, on_delete=models.CASCADE)
    total_marks        = models.IntegerField()
    total_questions    = models.IntegerField()
    duration           = models.DurationField(help_text="Test duration (hh:mm:ss)")
    is_results_visible = models.BooleanField(default=False)
    status             = models.BooleanField(default=False, help_text="False = Upcoming, True = Completed")
    user               = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.name} | {self.course.course_name if self.course else 'N/A'} | {self.batch.batch_name} | {self.total_marks} marks | {self.total_questions} questions"

class Question(models.Model):
    test        = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text        = models.TextField(help_text="The question text")
    marks       = models.IntegerField(default=1, help_text="Marks allocated for this question")
    num_choices = models.IntegerField(default=4, help_text="Number of choices for this question")

    def __str__(self):
        return f"Q: {self.text}"

class Choice(models.Model):
    question   = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text       = models.CharField(max_length=500, help_text="Choice text")
    is_correct = models.BooleanField(default=False, null=False, help_text="Indicates the correct answer")

    def __str__(self):
        return f"{self.question} | {self.text}"

class TestCode(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='access_codes')
    student_name = models.CharField(max_length=100, null=True, blank=True)
    student_email = models.EmailField(null=True, blank=True)
    code = models.CharField(max_length=10, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.code} - {self.student_name}"

    @classmethod
    def generate_code(cls):
        """Generate a unique 6-character code"""
        import random
        import string
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not cls.objects.filter(code=code).exists():
                return code

class TestAttempt(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='attempts')
    student_name = models.CharField(max_length=100, null=True, blank=True)
    student_email = models.EmailField(null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student_name} - {self.test.name}"

    def is_time_up(self):
        """Check if the test duration has expired"""
        if not self.end_time:
            duration = self.test.duration
            time_elapsed = timezone.now() - self.start_time
            return time_elapsed >= duration
        return True

class Answer(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.attempt} | {self.question} | {self.choice if self.choice else 'No Answer'}"
