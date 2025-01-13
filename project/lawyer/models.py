from django.conf import settings
from django.db import models
from django.db.models import Avg


# class Lawyer(models.Model):
#     name = models.CharField(max_length=100, verbose_name="Имя")
#     specialization = models.CharField(max_length=100, verbose_name="Специализация")
#     experience = models.IntegerField(verbose_name="Опыт работы (лет)")
#     photo = models.ImageField(upload_to='profile_images/', verbose_name="Фотография", null=True, blank=True)

#     def __str__(self):
#         return self.name

#     def average_rating(self):
#         """Возвращает средний рейтинг юриста."""
#         return self.reviews.aggregate(Avg('score'))['score__avg']

#     class Meta:
#         verbose_name = "Юрист"
#         verbose_name_plural = "Юристы"


class Lawyer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    specialization = models.CharField(max_length=100, verbose_name="Специализация")
    experience = models.IntegerField(verbose_name="Опыт работы (лет)")
    photo = models.ImageField(upload_to='profile_images/', verbose_name="Фотография", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона", null=True, blank=True)  # Новое поле
    email = models.EmailField(verbose_name="Электронная почта", null=True, blank=True)  # Новое поле

    def __str__(self):
        return self.name

    def average_rating(self):
        """Возвращает средний рейтинг юриста."""
        return self.reviews.aggregate(Avg('score'))['score__avg']

    class Meta:
        verbose_name = "Юрист"
        verbose_name_plural = "Юристы"

        
class Review(models.Model):
    lawyer = models.ForeignKey('Lawyer', on_delete=models.CASCADE, related_name='reviews', verbose_name="Юрист")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Текст отзыва", null=True, blank=True)  # Текст отзыва (необязательный)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Оценка")  # Оценка от 1 до 5
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ('lawyer', 'user')  # Один пользователь может оставить только один отзыв на юриста

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.lawyer.name} (Оценка: {self.score})"
