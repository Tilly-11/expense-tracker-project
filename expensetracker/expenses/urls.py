from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ExpenseViewSet, InsightsAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expenses')

urlpatterns = [
    path('', include(router.urls)),
    path('insights/', InsightsAPIView.as_view(), name='insights'),
    # Auth
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Optionally add registration endpoint
    path('auth/register/', views.register_view, name='register'),
]
