from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Plan, Subscription, Payment, Student, Profile, Course, Attendance
from django.utils import timezone
from .serializers import PlanSerializer, SubscriptionSerializer, PaymentSerializer, CourseSerializer
from django.shortcuts import get_object_or_404
import datetime, os, requests

@api_view(['GET'])
def health(request):
    return Response({'status':'ok'})

@api_view(['GET'])
def plans_list(request):
    plans = Plan.objects.all()
    return Response(PlanSerializer(plans, many=True).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_plan(request):
    # Create Payment record (Vodafone Cash manual)
    user = request.user
    plan_id = request.data.get('plan_id')
    plan = get_object_or_404(Plan, id=plan_id)
    amount = plan.price
    payment = Payment.objects.create(user=user, amount=amount, method='vodafone_cash', status='pending')
    # Return payment id to user to upload receipt
    return Response({'payment_id': payment.id, 'message':'Send Vodafone Cash payment and upload receipt for verification.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_receipt(request):
    payment_id = request.data.get('payment_id')
    file = request.FILES.get('receipt')
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    payment.receipt = file
    payment.status = 'waiting_verification'
    payment.save()
    return Response({'message':'Receipt uploaded. Admin will verify and activate subscription.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def scan_barcode(request):
    barcode = request.data.get('barcode')
    if not barcode:
        return Response({'detail':'barcode required'}, status=400)
    student = Student.objects.filter(barcode_id=barcode).first()
    if not student:
        return Response({'detail':'student not found'}, status=404)
    # get latest session
    session = student.user.enrollment_set.first() if False else None
    # simplified: mark attendance for last class
    last_session = Course.objects.first()
    attendance = Attendance.objects.create(student=student, class_session=student.enrollment_set.first().class_session if student.enrollment_set.exists() else None, present=True)
    return Response({'message':'attendance recorded'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_chat(request):
    # proxy to external AI provider using AI_API_KEY
    msg = request.data.get('message')
    api_key = os.getenv('AI_API_KEY')
    if not api_key:
        return Response({'error':'AI not configured'}, status=500)
    # Example: proxy to OpenAI chat completions (user to update URL/model as needed)
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {'Authorization': f'Bearer {api_key}'}
    payload = { 'model': 'gpt-4o-mini', 'messages':[{'role':'user','content': msg}] }
    r = requests.post(url, json=payload, headers=headers)
    return Response(r.json())
