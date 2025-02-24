from django.db import models
from django.utils.timezone import now

from django.conf import settings

EXCHANGE_API_URL = settings.EXCHANGE_API

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    rate = models.DecimalField(max_digits=10, decimal_places=6)
    last_updated = models.DateTimeField(default=now)

