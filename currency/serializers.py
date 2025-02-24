from rest_framework import serializers

class CurrencyConversionSerializer(serializers.Serializer):
    base_currency = serializers.CharField
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    target_currencies = serializers.ListField
