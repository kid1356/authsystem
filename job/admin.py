from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'Job_Title','user']

@admin.register(ApplyJob)
class ApplyJobAdmin(admin.ModelAdmin):
    list_display = ['id','user','get_job_title']
    
    def get_job_title(self, obj):
        return obj.JobId.Job_Title if obj.JobId else "No Job Title"

    get_job_title.short_description = 'Job Title'