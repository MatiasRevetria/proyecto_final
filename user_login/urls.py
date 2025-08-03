from django.urls import path
from .views import RegisterUserView, LoginUserView, LandingPageView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('', LandingPageView.as_view(), name='landing'),
]
