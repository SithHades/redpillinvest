from django.urls import path, include
from rest_framework.routers import DefaultRouter
from redpillinvest.api.views import CEOViewSet, StockViewSet, WatchlistViewSet, AdminViewSet

router = DefaultRouter()
router.register(r'ceos', CEOViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')
router.register(r'admin', AdminViewSet, basename='admin')

urlpatterns = [
    path('', include(router.urls)),
]
