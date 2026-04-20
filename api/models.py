from django.db import models
from django.utils.text import slugify


class Blog(models.Model):
    title        = models.CharField(max_length=255)
    slug         = models.SlugField(unique=True, blank=True)
    content      = models.TextField()
    cover_image  = models.ImageField(upload_to='blogs/')
    author       = models.CharField(max_length=100, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Enquiry_form(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name ='Enquiry'
        verbose_name_plural = 'Enquiries'
    
    

class Subscribers_Form(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name ='Subscriber'
        verbose_name_plural = 'Subscribers' 


class Rental_form(models.Model):

    ADMIN_STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('contacted', 'Contacted'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    first_name     = models.CharField(max_length=50)
    last_name      = models.CharField(max_length=50)
    email          = models.EmailField()
    phone          = models.CharField(max_length=50)
    address        = models.TextField()
    property_type  = models.CharField(max_length=50)
    current_status = models.CharField(max_length=50)
    bedrooms       = models.CharField(max_length=50)
    bathrooms      = models.CharField(max_length=50)
    appraisal_date = models.DateField()
    note           = models.TextField()
    status         = models.CharField(max_length=20, choices=ADMIN_STATUS_CHOICES, default='pending', verbose_name='Contact Status')
    submitted_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name        = 'Rental Appraisal'
        verbose_name_plural = 'Rental Appraisals'
        ordering            = ['-submitted_at']
    