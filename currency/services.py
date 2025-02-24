import requests
from django.utils.timezone import now, timedelta

from .models import Currency, EXCHANGE_API_URL



def update_exchange_rates():
        last_updated_entry = Currency.objects.order_by("-last_updated").first()
        
        if not last_updated_entry or last_updated_entry.last_updated < now() - timedelta(hours=2):
            response = requests.get(EXCHANGE_API_URL)
            if response.status_code != 200:
                return
            
            data = response.json().get("rates")
            base_usd = data.get("USD") 
  
            required_currencies = ["USD", "EUR", "RUB", "BYN"]
            for code in required_currencies:
                if code in data:
                    rate = data[code] / base_usd 
                    Currency.objects.update_or_create(code=code, defaults={"rate": rate, "last_updated": now()})

def fetch_exchange_rates():
    response = requests.get(EXCHANGE_API_URL)

    if response.status_code != 200:
        raise Exception("Failed to fetch exchange rates")

    data = response.json()
    rates = data.get("rates", {})

    usd_to_eur = rates.get("USD", 1)  
    adjusted_rates = {code: rate / usd_to_eur for code, rate in rates.items()} 

    for code, rate in adjusted_rates.items():
        Currency.objects.update_or_create(
            code=code, defaults={"rate": rate, "last_updated": now()}
        )


if not Currency.objects.exists():
    fetch_exchange_rates()
