from django.db import models

class Batch(models.Model):
    batch_name    = models.CharField(max_length = 255)
    batch_section = models.CharField(max_length = 3)
    batch_session = models.CharField(max_length = 20)
    semester      = models.IntegerField()

    def __str__(self):
        return f"{self.batch_name} | {self.batch_session} | {self.semester}th sem | {self.batch_section}"

class Course(models.Model):
    course_name = models.CharField(max_length = 255, unique = True)
    course_code = models.CharField(max_length = 255, unique = True)

    def __str__(self):
        return f"{self.course_name} | {self.course_code}"

class Test(models.Model):
    name               = models.CharField(max_length = 255)
    course             = models.ForeignKey(Course, on_delete = models.CASCADE, null=True, blank=True, default=None)
    batch              = models.ForeignKey(Batch, on_delete = models.CASCADE)
    total_marks        = models.IntegerField()
    total_questions    = models.IntegerField()
    duration           = models.DurationField()
    is_results_visible = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.name} | {self.course.course_name} |{self.batch.batch_name} | {self.total_marks} | {self.total_ques}"


    
