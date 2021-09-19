from django.db import models
import os
from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone

# Create your models here.


class Resume(models.Model):
    file = models.FileField(upload_to='')
    job = models.ForeignKey(
        'Job', blank=True, on_delete=models.CASCADE, related_name='jobResume', null=True)

    def get_path(self):
        return f'{self.file.url}'

    def __str__(self):
        return self.file.name

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        super(Resume, self).delete(*args, **kwargs)


class GeneralResume(models.Model):
    file = models.FileField(upload_to='general')
    date = models.DateField(auto_now_add=True)

    def get_path(self):
        return f'{self.file.url}'

    def __str__(self):
        return self.file.name

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        super(GeneralResume, self).delete(*args, **kwargs)


class Job(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    location = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    date = models.DateField(auto_created=True)


    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("jobListing", kwargs={"id": self.id})

    def delete(self, *args, **kwargs):
        for resume in self.jobResume.all():
            os.remove(os.path.join(settings.MEDIA_ROOT, resume.file.name))
        super(Job, self).delete(*args, **kwargs)
