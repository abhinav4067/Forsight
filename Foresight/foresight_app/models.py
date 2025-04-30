from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class StudentRegistration(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    qualification = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    # resume = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.full_name



# models.py
from django.db import models

class User_reg(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


from django.db import models

from django.db import models

class Post(models.Model):
    heading = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.heading

from django.db import models

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    replied = models.BooleanField(default=False)  # ✅ New field
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
