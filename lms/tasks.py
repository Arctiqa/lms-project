from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from lms.models import Course
from users.models import Subscription


@shared_task
def send_email_update_course(course_id):
    course = Course.objects.get(id=course_id)
    print(f'----{course}----')
    subscriptions = Subscription.objects.all().filter(course=course_id)
    for user in subscriptions:
        print('отправка письма-------------------------------w')
        print(user.user)
        message = f'Курс "{course.name}" был обновлен. Зайдите, чтобы увидеть новые материалы'
        send_mail(
            subject=course.name,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.user]
        )
