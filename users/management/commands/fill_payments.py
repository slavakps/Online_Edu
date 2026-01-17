from django.core.management.base import BaseCommand
from users.models import User, Payment
from materials.models import Course, Lesson

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Получаем объекты из базы
        user = User.objects.get(email='slavakpss99@bk.ru')
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        # Создаем платежи
        Payment.objects.create(
            user=user,
            paid_course=course,
            amount=15000.00,
            payment_method='transfer'
        )

        Payment.objects.create(
            user=user,
            paid_lesson=lesson,
            amount=3000.00,
            payment_method='cash'
        )

        self.stdout.write(
            self.style.SUCCESS('Успешно создано 2 тестовых платежа!')
        )