from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Plan, Subscription, Payment, Teacher, Course, ClassSession, Student, Enrollment, Attendance, Quiz, Question, Grade, Bonus, Deduction, Compensation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    class Meta:
        model = Subscription
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
