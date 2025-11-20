Django Backend for Institute Management (Starter)

Features included:
- Django + DRF
- Models: Users/Profiles, Plans, Subscriptions, Payments (Vodafone Cash manual), Courses, Teachers, Students, Enrollment, Attendance, Quiz, Grades, Bonus/Deduction/Compensation
- Admin site configuration for managing payments/approvals
- API endpoints: plans, buy-plan, upload-receipt, scan (barcode), ai/chat proxy
- Seed command: `python manage.py seed` creates superadmin and example plans

Quickstart:
1. copy .env.example to .env and edit
2. pip install -r requirements.txt
3. python manage.py migrate
4. python manage.py seed
5. python manage.py runserver

Note: Set AI_API_KEY in .env to enable AI proxy.
