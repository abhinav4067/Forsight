from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
class StudentRegistration(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)  
    phone = PhoneNumberField(region='IN', blank=True, null=True)
    whatsapp = PhoneNumberField(blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_phone = PhoneNumberField(blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mother_phone = PhoneNumberField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    qualification = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    address = models.TextField()
    adhaar_number = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    # Academic Info
    college_name = models.CharField(max_length=255, blank=True, null=True)
    college_year = models.CharField(max_length=10, blank=True, null=True)
    college_score = models.CharField(max_length=50, blank=True, null=True)
    school_12 = models.CharField(max_length=255, blank=True, null=True)
    year_12 = models.CharField(max_length=10, blank=True, null=True)
    score_12 = models.CharField(max_length=50, blank=True, null=True)
    school_10 = models.CharField(max_length=255, blank=True, null=True)
    year_10 = models.CharField(max_length=10, blank=True, null=True)
    score_10 = models.CharField(max_length=50, blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)

    # Work Experience
    company_name = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    work_from = models.CharField(max_length=50, blank=True, null=True)
    work_to = models.CharField(max_length=50, blank=True, null=True)


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

class PrivacyPolicy(models.Model):
    policy = models.TextField()

    def __str__(self):
        return f"Privacy Policy ({self.id})"

