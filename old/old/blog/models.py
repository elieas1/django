from django.db import models
from django.shortcuts import reverse
import os
from django.conf import settings

class Blog(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    date = models.DateField(auto_now_add=True)
    paragraph1 = models.TextField(blank=True, null=True)
    paragraph2 = models.TextField(blank=True, null=True)
    paragraph3 = models.TextField(blank=True, null=True)
    paragraph4 = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnail', null=True, blank=True)
    homepage = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("entry", args={self.slug})
    
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.thumbnail.name))
        super(Blog, self).delete(*args, **kwargs)


class Image(models.Model):
    image = models.ImageField(upload_to='images', null=True, blank=True)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        super(Image, self).delete(*args, **kwargs)

    def __str__(self):
        return os.path.basename(self.image.name)
