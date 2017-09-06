from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True)
    source = models.CharField(max_length=200, null=True)
    provider = models.CharField(max_length=200, null=True)
    language = models.CharField(max_length=200, null=True)
    duration = models.CharField(max_length=200, null=True)
    duration_filter = models.CharField(max_length=200, null=True)
    start_date = models.CharField(max_length=200, null=True)
    link = models.CharField(max_length=200, null=True)
    video = models.CharField(max_length=200, null=True)
    image = models.CharField(max_length=500, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    name = models.CharField(max_length=200, null=True)
    info = models.TextField(null=True)
    course = models.ManyToManyField(Course)

    def __str__(self):
        return self.name