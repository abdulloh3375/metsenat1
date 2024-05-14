from django.urls import path
from app1 import views 
from views import (SponsorsListAPI, SponsorCreateAPIView, SponsorUpdateAPIView,
                   StudentListAPI, StudentCreateAPIView, StudentUpdateAPIView, StudentDetailAPIView,
                   StudentSponsorListAPI, StudentSponsorCreateAPIView, StudentSponsorUpdateAPIView, StudentSponsorRetriveAPIView,
                   StatisticAPIView) 


urlpatterns = [
    path('sponsor-list/', SponsorsListAPI.as_view()),
    path('sponsor-create/', SponsorCreateAPIView.as_view()),
    path('sponsor-update/<int:pk>/', SponsorUpdateAPIView.as_view()),
    

    path('student-list/', StudentListAPI.as_view()),
    path('student-create/', StudentCreateAPIView.as_view()),
    path('student-retriece-update/', StudentDetailAPIView.as_view()),
    path('student-update/<int:pk>/', StudentUpdateAPIView.as_view()),

    path('studentsponsor-list/', StudentSponsorListAPI.as_view()),
    path('studentsponsor-create/', StudentSponsorCreateAPIView.as_view()),
    path('studentsponsor-update/<int:pk>/', StudentSponsorUpdateAPIView.as_view()),


    path('amount-statictic', StatisticAPIView.as_view()),
    
]