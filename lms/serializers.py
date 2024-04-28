from rest_framework import serializers, fields

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    def get_lessons_count(self, instance):
        return instance.lesson_set.all().count()

    class Meta:
        model = Course
        fields = ('id', 'name', 'lessons_count', 'lessons')
