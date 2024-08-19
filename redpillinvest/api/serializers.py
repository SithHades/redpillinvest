from rest_framework import serializers
from redpillinvest.api.models import CEO, Stock, Watchlist

class CEOSerializer(serializers.ModelSerializer):
    class Meta:
        model = CEO
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    ceo = CEOSerializer()

    class Meta:
        model = Stock
        fields = '__all__'

class WatchlistSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=True, read_only=True)

    class Meta:
        model = Watchlist
        fields = '__all__'