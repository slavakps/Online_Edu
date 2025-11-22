from rest_framework import viewsets, generics, permissions, status
from .models import Course, Lesson, Subscription
from users.models import Payment
from .stripe_service import create_product, create_price, create_checkout_session
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsSuperUser, IsModerator, IsOwner
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .paginators import MaterialsPaginator



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPaginator

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [permissions.IsAuthenticated, ~IsModerator]
        elif self.action in ['destroy']:
            permission_classes = [IsSuperUser | IsOwner]
        elif self.action == ['list']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner | IsSuperUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubscriptionAPIView(APIView):
    def post(self, request, course_id, *args, **kwargs):
        user = request.user
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MaterialsPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner | IsSuperUser]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, ~IsModerator]  # Создавать могут все авторизованные

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner | IsSuperUser]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsSuperUser]


class CoursePaymentView(APIView):
    def post(self, request):
        course_id = request.data.get('course_id')
        course = Course.objects.get(id=course_id)
        product = create_product(course.title, course.description)

        if product is None:
            return Response({"error": "Не удалось создать продукт в Stripe"}, status=400)

        price = create_price(product.id, course.price)
        if price is None:
            return Response({"error": "Не удалось создать цену в Stripe"}, status=400)

        session = create_checkout_session(
            price_id=price.id,
            success_url='https://example.com/success',
            cancel_url='https://example.com/cancel'
        )
        if session is None:
            return Response({"error": "Не удалось создать сессию оплаты"}, status=400)

        payment = Payment.objects.create(
            user=request.user,
            paid_course=course,
            amount=course.price,
            payment_method='stripe',
            stripe_product_id=product.id,
            stripe_price_id=price.id,
            stripe_session_id=session.id,
            stripe_payment_url=session.url
        )

        return Response({
            "payment_url": session.url
        })