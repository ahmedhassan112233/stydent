from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

ROLE_CHOICES = (
    ('superadmin','SuperAdmin'),
    ('admin','Admin'),
    ('teacher','Teacher'),
    ('student','Student'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    full_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    barcode_id = models.CharField(max_length=200, blank=True, null=True, unique=True)
    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Plan(models.Model):
    key = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField(default=30)
    features = models.JSONField(blank=True, null=True)
    def __str__(self):
        return self.title

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    started_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    status = models.CharField(max_length=30, default='active')
    provider_payment_id = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.key} - {self.status}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, default='vodafone_cash')
    status = models.CharField(max_length=30, default='pending')
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    gateway_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Payment {self.id} - {self.user.username} - {self.status}"

class Teacher(models.Model):
    full_name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.full_name

class Course(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.title

class ClassSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return f"{self.course.title} - {self.start_time}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parent_phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    barcode_id = models.CharField(max_length=200, blank=True, null=True, unique=True)
    def __str__(self):
        return self.user.username

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return f"{self.student} -> {self.class_session}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    present = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.student} - {self.class_session} - {self.present}"

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    time_limit_minutes = models.IntegerField(default=30)
    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    choices = models.JSONField()  # list of choices
    correct = models.IntegerField()  # index of correct choice
    def __str__(self):
        return f"Q: {self.text[:30]}"

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Bonus(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Deduction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Compensation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    deduction = models.ForeignKey(Deduction, on_delete=models.CASCADE)
    bonus = models.ForeignKey(Bonus, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
