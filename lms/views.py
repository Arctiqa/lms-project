from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from lms.models import Course, Lesson
from lms.paginators import CourseLessonPaginator
from lms.serializers import CourseSerializer, LessonSerializer
from lms.tasks import send_email_update_course
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CourseLessonPaginator

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ['retrieve', 'update', 'partial_update', 'list']:
            self.permission_classes = (IsAuthenticated | IsModerator | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (IsAuthenticated, ~IsModerator, IsOwner,)
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        course = serializer.save()
        send_email_update_course.delay(course.id)


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, AllowAny, IsModerator | IsOwner]
    pagination_class = CourseLessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]
