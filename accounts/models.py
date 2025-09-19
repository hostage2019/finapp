from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField 
from pilkit.processors import ResizeToFill

from bank.models import AccType

# Create your models here.

class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=255, default='')
    birth_date = models.DateField(null=True, blank=True)
    currentBalance = models.DecimalField(max_digits=65, decimal_places=2,default=0.00)
    accType = models.ForeignKey(AccType, on_delete=models.PROTECT,null=True, blank=True)
    image = ProcessedImageField(blank=True, null=True,default='profile/metrologo.png', upload_to='profile',processors=[ResizeToFill(100, 100)],format='JPEG',options={'quality': 60})


class Transaction(models.Model):
    date = models.DateField()
    time = models.TimeField(auto_now_add=True)
    activity = models.CharField(max_length=60, null=True, blank=True)
    amount = models.DecimalField(max_digits=65, decimal_places=2,default=0.00)
    updatedBy = models.CharField(max_length=60)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=True, null=True)