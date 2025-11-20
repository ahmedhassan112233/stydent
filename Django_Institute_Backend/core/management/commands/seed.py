from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Plan, Profile
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed initial data: superadmin and plans'

    def handle(self, *args, **options):
        if not User.objects.filter(username='superadmin').exists():
            u = User.objects.create_superuser('superadmin', 'admin@center.com', 'StrongP@ss123')
            Profile.objects.filter(user=u).update(role='superadmin')
            self.stdout.write(self.style.SUCCESS('Superadmin created: superadmin / StrongP@ss123'))

        plans = [
            {'key':'trial','title':'Trial 7 days','price':0,'duration_days':7},
            {'key':'monthly','title':'Monthly Plan','price':100,'duration_days':30},
            {'key':'yearly','title':'Yearly Plan','price':1000,'duration_days':365},
        ]
        for p in plans:
            Plan.objects.get_or_create(key=p['key'], defaults=p)
        self.stdout.write(self.style.SUCCESS('Plans seeded'))
