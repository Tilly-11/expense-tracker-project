# expenses/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta, date
from rest_framework.views import APIView
from django.db.models.functions import TruncMonth, TruncWeek
from .ai_utils import predict_category
from .ai.anomaly import detect_anomalies_for_user

from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from django.db import IntegrityError

# drf-spectacular imports for API docs
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.openapi import OpenApiParameter

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class RegisterResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()


@extend_schema(
    request=RegisterSerializer,
    responses={
        201: RegisterResponseSerializer,
        400: OpenApiResponse(description="Username already exists")
    },
    description="Register a new user with username and password"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    s = RegisterSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    
    try:
        u = User.objects.create_user(
            username=s.validated_data['username'],
            password=s.validated_data['password']
        )
        return Response({'id': u.id, 'username': u.username}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response(
            {"error": "Username already exists"}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # serializer.create handles AI logic already
        serializer.save()

    @extend_schema(
        request=ExpenseSerializer,
        responses=ExpenseSerializer,
        description=(
            "Create expense. If `category` is omitted, AI will predict it and "
            "`predicted_category`/`ai_confidence` will be set. "
            "User override is possible via PATCH or the override action."
        ),
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def override(self, request, pk=None):
        """
        Endpoint to manually set/override category:
        POST /api/expenses/{id}/override/ { "category": "Shopping" }
        """
        expense = self.get_object()
        category = request.data.get('category')
        if not category:
            return Response({'detail': 'category required'}, status=status.HTTP_400_BAD_REQUEST)
        expense.category = category
        expense.user_override = True
        expense.save()
        return Response(ExpenseSerializer(expense).data)


class InsightsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=dict,
                description="Insights: weekly/monthly/top_categories/anomalies"
            )
        },
        description="Returns summaries and anomaly detection for the authenticated user."
    )
    def get(self, request):
        user = request.user
        today = date.today()

        # Last 30 days weekly summary
        last_30 = today - timedelta(days=30)
        q = Expense.objects.filter(user=user, date__gte=last_30)
        weekly_qs = (
            q.annotate(week=TruncWeek('date'))
             .values('week')
             .annotate(total=Sum('amount'))
             .order_by('week')
        )
        weekly = [
            {'week': w['week'].isoformat(), 'total': float(w['total'] or 0)}
            for w in weekly_qs
        ]

        # monthly summary (last 6 months)
        six_months_ago = today - timedelta(days=180)
        q2 = Expense.objects.filter(user=user, date__gte=six_months_ago)
        monthly_qs = (
            q2.annotate(month=TruncMonth('date'))
              .values('month')
              .annotate(total=Sum('amount'))
              .order_by('month')
        )
        monthly = [
            {'month': m['month'].isoformat(), 'total': float(m['total'] or 0)}
            for m in monthly_qs
        ]

        # top categories (all time)
        top_cat_qs = (
            Expense.objects.filter(user=user)
            .values('category')
            .annotate(total=Sum('amount'))
            .order_by('-total')[:5]
        )
        top_categories = [
            {'category': c['category'] or 'Uncategorized', 'total': float(c['total'] or 0)}
            for c in top_cat_qs
        ]

        # Use the more sophisticated anomaly detection
        anomalies = detect_anomalies_for_user(user)

        return Response({
            'weekly': weekly,
            'monthly': monthly,
            'top_categories': top_categories,
            'anomalies': anomalies
        })