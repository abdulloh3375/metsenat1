from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from . import models
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from . import serializers
from rest_framework.views import APIView,Response
from django.db.models import Sum
from datetime import datetime


"""
This three classes are for Sponson

"""
class SponsorsListAPI(ListAPIView):
    queryset = models.Sponsor.objects.all()
    serializer_class = serializers.SponsorSerializer


class SponsorCreateAPIView(CreateAPIView):
    serializer_class = serializers.SponsorSerializer
    queryset = models.Sponsor.objects.all()
    

class SponsorUpdateAPIView(UpdateAPIView):
    serializer_class = serializers.SponsorSerializer
    queryset = models.Sponsor.objects.all()



"""
This three classes are for Student

"""
class StudentListAPI(ListAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    filter_backends =[DjangoFilterBackend,]
    filterset_fields = ('student_type', 'university')
    search_fields = ('full_name',)


class StudentCreateAPIView(CreateAPIView):
    serializer_class = serializers.StudentSerializer
    queryset = models.Student.objects.all()


class StudentUpdateAPIView(UpdateAPIView):
    serializer_class = serializers.StudentSerializer
    queryset = models.Student.objects.all()


class StudentDetailAPIView(RetrieveAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentDetailSerializer



"""
This three classes are for University

"""
class UniversityListAPI(ListAPIView):
    queryset = models.University.objects.all()
    serializer_class = serializers.UniversitySerializer



"""
This three classes are for StudentSponsor

"""
class StudentSponsorListAPI(ListAPIView):
    queryset = models.StudentSponsor.objects.all()
    serializer_class = serializers.StudentSponsorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ('student_type', 'university')
    search_fields = ('full_name',)


class StudentSponsorCreateAPIView(CreateAPIView):
    serializer_class = serializers.StudentSponsorSerializer
    queryset = models.StudentSponsor.objects.all()


class StudentSponsorUpdateAPIView(UpdateAPIView):
    serializer_class = serializers.StudentSponsorSerializer
    queryset = models.StudentSponsor.objects.all()


class StudentSponsorRetriveAPIView(RetrieveAPIView):
    serializer_class = serializers.StudentSponsorSerializer
    queryset = models.StudentSponsor.objects.all()



"""
This class for analys of statistic

"""
class StatisticAPIView(APIView):
   
    def get(self, request):
        total_paid_sum = models.StudentSponsor.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        total_required_sum = models.Student.objects.aggregate(total_amount=Sum('contract'))['total_amount'] or 0
        total_unpaid_sum = 0
        
        return Response(
            data={
                "total_paid_sum": total_paid_sum,
                "total_required_sum": total_required_sum,
                "total_unpaid_sum": total_unpaid_sum
            }
        )
    


"""
This class for create a grafic for statistic

"""
class GraficAPIView(APIView):

    def get(self, request):
        from datetime import datetime
        this_year = datetime.now().year

        result = []
        for i in range(1,13):
            sponsor_amount = models.Sponsor.objects.filter(
                created_at__month = i,
                created_at__year = this_year,
                status = 'confirm'  
            ).aggregate(total=Sum('amount'))["total"] or 0

            student_amount = models.Sponsor.objects.filter(
                created_at__month = i,
                created_at__year = this_year 
            ).aggregate(total=Sum('contract'))["total"] or 0
            result.append({
                "month": i,
                "sponsor_amount": sponsor_amount,
                "student_amount": student_amount
            })
        return Response(result)


