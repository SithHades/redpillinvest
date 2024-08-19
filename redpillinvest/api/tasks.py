from celery import shared_task
from redpillinvest.api.models import CEO, Stock

@shared_task
def update_database(update_type='all'):
    if update_type in ['all', 'ceos']:
        CEOs = CEO.objects.all()
        for ceo in CEOs:
            ceo.update()
    if update_type in ['all', 'stocks']:
        stocks = Stock.objects.all()
        for stock in stocks:
            stock.update()
    return 'Database update completed'