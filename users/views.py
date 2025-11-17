from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework.decorators import permission_classes
from .models import Payment, User
from rest_framework import viewsets, filters, permissions, generics
from materials.serializers import PaymentSerializer
from .serializers import UserSerializer, UserRegistrationSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

