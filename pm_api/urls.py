from django.urls import path

from pm_api.views import HelloApiView, UserProfileSignUpView, UserProfileSignInView, WishlistView


urlpatterns = [
    path('hello-view/', HelloApiView.as_view()),
    path('user/signin/', UserProfileSignInView.as_view()),
    path('user/signup/', UserProfileSignUpView.as_view()),
    path('user/wishlist/', WishlistView.as_view()),
]