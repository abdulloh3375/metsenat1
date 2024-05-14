from rest_framework.serializers import ModelSerializer
from . import models
from rest_framework import serializers
from django.db.models import Sum



class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaseModel
        fields = '__all__'


        
class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sponsor
        field = "__all__"



class StudentSerializer(serializers.ModelSerializer):
    university = serializers.StringRelatedField(source = "university.title")
    allocated_amount = serializers.SerializerMethodField()
    
    def get_allocated_amount(self, obj):
        from django.db.models import Sum
        student_paid_money = obj.student_sponsors.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        return student_paid_money
    
    class Meta:
        model = models.Student
        exclude = ("created_at", "updated_at")
       



class StudentDetailSerializer(serializers.ModelSerializer):
    university = serializers.StringRelatedField(source = "university.title")
    class Meta:
        model = models.Student
        exclude = ("created_at", "update_at")   



class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.University
        fields = '__all__'



class StudentSponsorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StudentSponsor
        fields = '__all__'

        def validate(self, attrs):
            amount = attrs.get('amount')
            sponsor = attrs.get('sponsor')
            student = attrs.get('student')
            

            student_paid_money = student.student_sponsors.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0


            if student.contract - student_paid_money < amount:
                # raise serializers.ValidationError(detail={'error': f"Siz {student.contract - student_paid_money} pul to'lasangiz yetarli"})
                print('aaa')
                raise serializers.ValidationError(f"Yetarli mablag' mavjud emas. Siz {student.contract - student_paid_money} pul to'lasangiz yetarli")
            
            sponsor_paid_money = sponsor.student_sponsors.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0
            if sponsor.amount - sponsor_paid_money < amount:
                print('bbb')
                # raise serializers.ValidationError(
                #     detail={'error':
                #              f"Sizning xisobingizda {sponsor.amount - sponsor_paid_money} pul bor"})
                raise serializers.ValidationError(f"Xisobingizda yetarli mablag' mavjud emas. Sizning xisobingizda {sponsor.amount - sponsor_paid_money} pul bor")
            
            return attrs
