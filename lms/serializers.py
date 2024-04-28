from rest_framework import serializers

from lms.models import Course, Lesson
# from users.models import Payment
# from users.serializers import PaymentSerializer


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    # payment_info = serializers.SerializerMethodField()
    #
    # def get_payment_info(self, obj):
    #     payments = Payment.objects.filter(paid_course=obj)
    #     return PaymentSerializer(payments, many=True).data

    def get_lessons_count(self, instance):
        return instance.lesson_set.all().count()

    class Meta:
        model = Course
        fields = ('id', 'name', 'lessons_count', 'lessons')  # payment_info
