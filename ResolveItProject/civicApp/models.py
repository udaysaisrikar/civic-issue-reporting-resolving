from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Municipality(models.Model):
    mun_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True, blank=True)
    dept_name = models.CharField(max_length=100)
    head_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)

class Complaints(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    c_id = models.AutoField(primary_key=True)
    description = models.TextField()
    image = models.ImageField(upload_to='complaints/')
    latitude = models.FloatField()
    longitude = models.FloatField()
    municipality = models.ForeignKey('Municipality', null=True, blank=True, on_delete=models.SET_NULL)
    worker_name = models.CharField(max_length=100, null=True, blank=True)
    worker_num = models.CharField(max_length=10, null=True, blank=True)
    dept = models.CharField(max_length=100, default='General Department')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    resolved_image = models.ImageField(upload_to='resolved/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.resolved_image:
            self.status = 'RESOLVED'
        elif self.worker_name:
            self.status = 'IN_PROGRESS'
        else:
            self.status = 'PENDING'
        super().save(*args, **kwargs)


