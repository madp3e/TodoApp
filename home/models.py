from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.

class List(models.Model):
    content = models.CharField(max_length=50)
    created_date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content + " | " + str(self.completed)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pics", default="default.png")

    def __str__(self):
        return "{}`s Profile".format(self.user.username)

    # def save(self, *arg, **kwargs):
    #     super().save(*arg, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


