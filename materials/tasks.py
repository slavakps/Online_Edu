from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from core import settings
from .models import Course, Subscription


@shared_task
def block_inactive_users():
    """
    Фоновая задача: блокирует пользователей,
    которые не заходили более месяца
    """
    User = get_user_model()

    # Дата месяц назад
    month_ago = timezone.now() - timedelta(days=30)

    # Находим активных пользователей с last_login больше месяца назад
    inactive_users = User.objects.filter(
        is_active=True,  # только активных
        last_login__lt=month_ago  # не заходили больше месяца
    )

    # Блокируем (деактивируем)
    blocked_count = inactive_users.update(is_active=False)

    return f'Заблокировано пользователей: {blocked_count}'


@shared_task
def send_course_update_notification(course_id):
    """Асинхронная рассылка писем об обновлении курса"""
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course)

        for subscription in subscriptions:
            subject = f'Обновление курса: {course.title}'
            message = f'Курс "{course.title}" был обновлен. Зайдите на платформу чтобы увидеть изменения.'

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscription.user.email],
                fail_silently=True,
            )

        return f'Уведомления отправлены {subscriptions.count()} подписчикам'
    except Course.DoesNotExist:
        return 'Курс не найден'