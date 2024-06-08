from django.urls import path

from pm_api.views import HelloApiView


urlpatterns = [
    path('hello-view/', HelloApiView.as_view())
]