from rest_framework import serializers
from .models import *
from systemauth.models import User


class JobSerailizer(serializers.ModelSerializer):
    posted_by = serializers.SerializerMethodField('get_posted_by')
    applicants = serializers.SerializerMethodField('get_applicants')
    applied_by = serializers.SerializerMethodField('get_applied_by')

    class Meta:
        model = Job
        fields = ['id','user','posted_by','Job_Title','Job_Type','Job_Discription','is_approved','applicants','applied_by']
        extra_kwargs = {
            'user':{'required':True},
            'Job_Title':{'required':True},
            'Job_Type':{'required':True},
        }
  
    def get_applicants(self, instance):
        return instance.jobId.count()
    
    def get_posted_by(self,obj):
        try:
            user_id = obj.user_id
            user = User.objects.get(id= user_id)
            return {
            'name':user.name,
            'email': user.email,
               }
        except User.DoesNotExist:
            return{
                'User': "not found"
            }
    
    def get_applied_by(self,obj):
        applied_by = ApplyJob.objects.filter(JobId = obj)

        return [
            {   'id' :applicant.user.id,
                'name': applicant.user.name,
                'email': applicant.user.email,
                'is_approved': applicant.is_approved,
            }
            for applicant in applied_by
        ]
    
   
    

class ApplyJobSerializer(serializers.ModelSerializer):
    applied = serializers.SerializerMethodField('applied_by')
    class Meta:
        model = ApplyJob
        fields = ['id','user','JobId','file','is_approved','applied']
        extra_kwargs = {
            'JobId':{'required':True},
            'user':{'required':True},
        }

    def applied_by(self,obj):

        return [
            {
                'name':obj.user.name
            }
        ]

