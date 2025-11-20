from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health),
    path('plans/', views.plans_list),
    path('buy-plan/', views.buy_plan),
    path('upload-receipt/', views.upload_receipt),
    path('scan/', views.scan_barcode),
    path('ai/chat/', views.ai_chat),
]
