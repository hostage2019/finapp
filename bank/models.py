from django.db import models


# Create your models here.
class AccType(models.Model):
    accTypeName = models.CharField(max_length=100, verbose_name="AccountType", unique=True, default='')

    def __str__(self):
        return self.accTypeName



class Enquiry(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    sender = models.EmailField()

