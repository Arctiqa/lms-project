from django.utils import timezone

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=20, verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='avatars', default='avatars/default.jpg', verbose_name='аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(default=timezone.now, verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, related_name='payment')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, related_name='payment')
    payment_amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=10, choices=[('cash', 'наличные'), ('transfer', 'перевод')],
                                      verbose_name='способ оплаты')
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='id сессии',
        help_text='укажите id сессии'
    )
    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name='ссылка на оплату',
        help_text='укажите ссылку на оплату'
    )

    def __str__(self):
        return (f'{self.user} - {self.payment_date} - {self.payment_amount}:'
                f'{self.paid_course if self.paid_course else self.paid_lesson}')

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ['-payment_date']


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='подписчик')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'подписчик'
        verbose_name_plural = 'подписчики'
