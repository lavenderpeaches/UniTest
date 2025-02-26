from django.contrib import admin
from .models import Batch, Course, Test

# Register models
admin.site.register(Batch)
admin.site.register(Course)
admin.site.register(Test)
