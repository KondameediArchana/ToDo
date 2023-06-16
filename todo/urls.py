from django.urls import path
from .views import Details
from todo import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
path('Details/', Details.as_view()),
path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
path('data/', views.DataView.as_view(), name='data'),
]