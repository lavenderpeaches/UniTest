from django.contrib import admin
from .models import Batch, Course, Test, Question, Choice, TestCode, TestAttempt, Answer

# Register models
admin.site.register(Batch)
admin.site.register(Course)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(TestCode)
admin.site.register(TestAttempt)
admin.site.register(Answer)