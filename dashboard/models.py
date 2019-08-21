from django.db import models
from django.contrib.auth.models import User
from quiz.models import Category
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mycourse = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=100,blank=True)
    country = models.CharField(max_length=100,blank=True)
    image = models.ImageField(default='profile_pics/blank.png', upload_to='profile_pics')

    def __str__(self):
        return self.user.username

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (50, 50)
            img.thumbnail(output_size)
            img.save(self.image.path)
