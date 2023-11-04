from django.db import models
from systemauth.models import User
# Create your models here.


class Job(models.Model):
    Job_Title = models.CharField(max_length=255, null=True, blank=True)
    Job_Type = models.CharField(max_length=255, null=True, blank=True)
    Job_Discription = models.TextField(max_length=10000, null=True)
    is_approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    
    
    
    


class ApplyJob (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='userId')
    JobId = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, related_name='jobId')
    file = models.TextField(max_length=10000, null=True)
    is_approved = models.BooleanField(default=False)
    
    