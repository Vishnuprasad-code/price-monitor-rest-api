from celery import shared_task
from pm_api.models import Wishlist, PriceHistory, Product

from pm_api.random_history import create_random_history


@shared_task
def test_periodic_task():
    print('WORKS!!!!')

@shared_task
def update_price_tables():
    print('Updating Prices...')
    products = Product.objects.filter(wishlist__isnull=False).distinct()
    for product in products:
        PriceHistory.objects.create(
            price=create_random_history(),
            currency='INR',
            product=product
        )
    print('Finished Updating Prices!')