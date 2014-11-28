from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone

#User = get_user_model() Не запускает на Django 1.7
now  = timezone.now()