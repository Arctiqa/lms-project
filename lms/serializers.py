from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import URLCheckValidator
from users.models import Subscription


# from users.models import Payment
# from users.serializers import PaymentSerializer


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            URLCheckValidator(field='url')
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    course_subscription = serializers.SerializerMethodField(read_only=True)

    # payment_info = serializers.SerializerMethodField()
    #
    # def get_payment_info(self, obj):
    #     payments = Payment.objects.filter(paid_course=obj)
    #     return PaymentSerializer(payments, many=True).data

    def get_lessons_count(self, instance):
        return instance.lesson_set.all().count()

    def get_course_subscription(self, instance):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=instance).exists()
        return False

    class Meta:
        model = Course
        fields = ('id', 'name', 'lessons_count', 'lessons', 'course_subscription')  # payment_info


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
