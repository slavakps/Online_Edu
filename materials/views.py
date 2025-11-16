from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import permission_classes
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsSuperUser, IsModerator, IsOwner

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [permissions.IsAuthenticated]  # Создавать могут все авторизованные
        elif self.action in ['destroy']:
            permission_classes = [IsSuperUser]  # Удалять только админы
        else:
            permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner | IsSuperUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner | IsSuperUser]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner | IsSuperUser]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]  # Создавать могут все авторизованные

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