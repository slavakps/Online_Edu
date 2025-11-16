from rest_framework import serializers
from .models import Course, Lesson, Subscription
from users.models import Payment
from .validators import validate_youtube_url




class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lessons.all')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'