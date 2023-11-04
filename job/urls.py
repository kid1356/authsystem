from django.urls import path
from . import views


urlpatterns = [
   path('job/', views.JobView.as_view(), name='jobViewpost'),
   path('patchjob/<int:pk>/<int:user_id>', views.PatchJobView.as_view(), name='Patchviewget'),
   path('Detailjob/<int:pk>', views.DetailJobView.as_view(), name='Detailviewget'),
   path('Deletejob/<int:pk>', views.DeleteJobView.as_view(), name= 'deleteJob'),
   path('applyjob/', views.ApplicantsJobView.as_view(), name='applicantpost' ),
   path('applyjob/<int:pk>', views.DetailApplicantJobView.as_view(), name= 'detailapplicantviweget'),
   path('approved/applicants', views.ApprovedApplicantsView.as_view(), name = 'approved_applicants'),
   
   # path('getjob',views.GetJobView.as_view({'get': 'list','post': 'create','delete':'delete'}), name='job'),
]