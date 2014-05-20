from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone

User = get_user_model()
now  = timezone.now()