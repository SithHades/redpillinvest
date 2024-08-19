from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from redpillinvest.api.filters import StockFilter
from redpillinvest.api.models import CEO, Stock, Watchlist
from redpillinvest.api.serializers import CEOSerializer, StockSerializer, WatchlistSerializer
from redpillinvest.api.permissions import IsAdminOrReadOnly
from redpillinvest.api.tasks import update_database

class CEOViewSet(viewsets.ModelViewSet):
    queryset = CEO.objects.all()
    serializer_class = CEOSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'company']
    filterset_fields = ['age', 'tenure', 'company', 'education', 'country_of_origin']


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['symbol', 'name']
    filterset_class = StockFilter

    @action(detail=False, methods=['post'])
    def filter(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class WatchlistViewSet(viewsets.ModelViewSet):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add_stock(self, request):
        stock_id = request.data.get('stock_id')
        if not stock_id:
            return Response({'error': 'stock_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        watchlist, created = Watchlist.objects.get_or_create(user=request.user)
        stock = Stock.objects.get(id=stock_id)
        watchlist.stocks.add(stock)
        
        serializer = self.get_serializer(watchlist)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def remove_stock(self, request):
        stock_id = request.data.get('stock_id')
        if not stock_id:
            return Response({'error': 'stock_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        watchlist = Watchlist.objects.get(user=request.user)
        stock = Stock.objects.get(id=stock_id)
        watchlist.stocks.remove(stock)
        
        serializer = self.get_serializer(watchlist)
        return Response(serializer.data)
    

class AdminViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=['post'])
    def update_data(self, request):
        update_type = request.data.get('update_type', 'all')
        task = update_database.delay(update_type)
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['get'])
    def update_status(self, request):
        # TODO check if update is done.
        return Response({'status': 'done'}, status=status.HTTP_202_ACCEPTED)