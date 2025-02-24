from django.urls import path
from .views import ConvertCurrencyView

urlpatterns = [
    path("convert/", ConvertCurrencyView.as_view(), name="convert_currency"),
]