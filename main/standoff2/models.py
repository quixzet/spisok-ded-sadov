from django.db import models

class Kindergarten(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    address = models.TextField(verbose_name="Адрес")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    capacity = models.IntegerField(verbose_name="Вместимость (детей)", default=0)
    age_group = models.CharField(
        max_length=50,
        choices=[
            ('1.5-3', '1.5–3 года'),
            ('3-7', '3–7 лет'),
            ('1.5-7', '1.5–7 лет'),
        ],
        verbose_name="Возрастная группа"
    )
    work_hours = models.CharField(max_length=100, blank=True, null=True, verbose_name="Режим работы")
    photo = models.ImageField(upload_to='kindergartens/', blank=True, null=True, verbose_name="Фото")

    class Meta:
        verbose_name = "Детский сад"
        verbose_name_plural = "Детские сады"

    def __str__(self):
        return self.name
    