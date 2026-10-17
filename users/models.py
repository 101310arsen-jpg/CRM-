from django.contrib.auth.models import AbstractUser
from django.db import models


class Student(AbstractUser):
    GENDER_CHOICES = [('М', 'Мужской'), ('Ж', 'Женский')]
    STATUS_CHOICES = [
        ('обучается', 'Обучается'),
        ('академический отпуск', 'Академический отпуск'),
        ('отчислен', 'Отчислен'),
        ('выпускник', 'Выпускник'),
    ]
    EDUCATION_FORM_CHOICES = [
        ('очная', 'Очная'),
        ('заочная', 'Заочная'),
        ('вечерняя', 'Вечерняя'),
    ]
    FUNDING_CHOICES = [('бюджет', 'Бюджет'), ('контракт', 'Контракт')]
    COURSE_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4')]

    middle_name = models.CharField('Отчество', max_length=100, blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICES, default='М')
    phone = models.CharField('Телефон', max_length=20, blank=True)
    address = models.TextField('Адрес', blank=True)
    photo = models.ImageField('Фото', upload_to='students/', blank=True, null=True)
    student_id = models.CharField('Номер студенческого билета', max_length=20, unique=True)
    group = models.CharField('Группа', max_length=20)
    specialty = models.CharField('Специальность', max_length=150)
    course = models.PositiveSmallIntegerField('Курс', choices=COURSE_CHOICES, default=1)
    admission_year = models.PositiveSmallIntegerField('Год поступления', default=2024)
    education_form = models.CharField('Форма обучения', max_length=20, choices=EDUCATION_FORM_CHOICES, default='очная')
    funding = models.CharField('Основа обучения', max_length=20, choices=FUNDING_CHOICES, default='бюджет')
    status = models.CharField('Статус', max_length=30, choices=STATUS_CHOICES, default='обучается')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email', 'student_id']

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['last_name', 'first_name']

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'.strip()

    def __str__(self):
        return f'{self.full_name} ({self.group})'