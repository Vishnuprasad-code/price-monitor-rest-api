from celery import shared_task


@shared_task
def test_periodic_task():
    print('WORKS!!!!')