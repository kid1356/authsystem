from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,generics,viewsets
from .serializers import *
# Create your views here.

class JobView(APIView):
    def post(self, request):

        serializer = JobSerailizer(data = request.data)
    
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({"Posted successfully":serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({"Wrong requested":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    


class PatchJobView(APIView):
    def patch(self, request,pk,user_id):
        try:
            job = Job.objects.get(pk = pk)
        
        except Job.DoesNotExist:
            return Response("job Does not exists",status=status.HTTP_404_NOT_FOUND)
        
        print('JOb_user..........',job.user)
        print('request_user...........',request.user)
        if job.user != request.user:
            return Response("You are not authorized to change anything", status=status.HTTP_403_FORBIDDEN)
        
        try:
           applicants = ApplyJob.objects.get(JobId = job, user_id = user_id,is_approved = False)
           applicants.is_approved = True
           applicants.save()
        
           return Response("approved suucessfully", status = status.HTTP_200_OK)
        except ApplyJob.DoesNotExist:
            return Response('Applicant Not Found Or Already Approved', status=status.HTTP_404_NOT_FOUND)


class DetailJobView(APIView):

    def get(self, request,pk):
        try:
          job = Job.objects.get(pk=pk)

        except Job.DoesNotExist:
            return Response("no Job Found",status=status.HTTP_404_NOT_FOUND)
        
        serializer = JobSerailizer(job)
        return Response({'Apply_job_data':serializer.data}, status=status.HTTP_200_OK)
    

class DeleteJobView(generics.DestroyAPIView):
    queryset =  Job.objects.all()
    serializer_class = JobSerailizer

class ApplicantsJobView(APIView):
    
    def post(self, request):
        serializer = ApplyJobSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({'apply successfully': serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({'something Went wrong',serializer.errors},status=status.HTTP_400_BAD_REQUEST)



class DetailApplicantJobView(APIView):

    def get(self,request,pk):
        try:
            applyjob = ApplyJob.objects.get(pk= pk)
        except ApplyJob.DoesNotExist:
            return Response("not found", status=status.HTTP_404_NOT_FOUND)
        serializer = ApplyJobSerializer(applyjob)

        return Response({'data':serializer.data}, status=status.HTTP_200_OK)
        

class ApprovedApplicantsView(APIView):

    def get(self, request):
        jobs = Job.objects.filter(user=request.user)
        job_ids = jobs.values_list('id', flat=True)
        approved_applicants = ApplyJob.objects.filter(JobId__in = job_ids, is_approved  = True)
        serializer = ApplyJobSerializer(approved_applicants, many = True)
        return Response({'Approved Applicants ':serializer.data})
