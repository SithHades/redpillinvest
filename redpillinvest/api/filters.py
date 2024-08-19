import django_filters
from redpillinvest.api.models import Stock, CEO

class StockFilter(django_filters.FilterSet):
    ceo_age_min = django_filters.NumberFilter(field_name='ceo__age', lookup_expr='gte')
    ceo_age_max = django_filters.NumberFilter(field_name='ceo__age', lookup_expr='lte')
    ceo_tenure_min = django_filters.NumberFilter(field_name='ceo__tenure', lookup_expr='gte')
    ceo_tenure_max = django_filters.NumberFilter(field_name='ceo__tenure', lookup_expr='lte')
    ceo_education = django_filters.CharFilter(field_name='ceo__education', lookup_expr='icontains')
    ceo_previous_companies_count = django_filters.NumberFilter(method='filter_previous_companies_count')

    class Meta:
        model = Stock
        fields = ['sector', 'industry']

    def filter_previous_companies_count(self, queryset, name, value):
        return queryset.filter(ceo__previouse_companies__len=value)
