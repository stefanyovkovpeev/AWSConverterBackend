from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Currency
from .services import update_exchange_rates 

class ConvertCurrencyView(APIView):

    def post(self, request):

        # Checks database, if no values or older than 2 hours, fetches new ones
        update_exchange_rates()

        base_currency = request.data.get("base_currency")
        amount = request.data.get("amount")
        target_currencies = request.data.get("target_currencies", [])

        try:
            amount = Decimal(amount)
            
            base_rate = Currency.objects.get(code=base_currency).rate
            
            conversions = {}

            for code in target_currencies:
                try:
                    target_rate = Currency.objects.get(code=code).rate
                    converted_amount = amount * (target_rate / base_rate)
                    conversions[code] = round(converted_amount, 2)
                except Currency.DoesNotExist:
                    conversions[code] = "Currency not found"

            return Response({"converted_values": conversions})

        except:
            return Response(
                {"error": "Something Went Wrong."},
                status=status.HTTP_400_BAD_REQUEST
            )