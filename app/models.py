from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator


class KindergartenImage(models.Model):
    kindergarten = models.ForeignKey('Kindergarten', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='kindergartens/images/', verbose_name='Изображение')
    caption = models.CharField(max_length=200, blank=True, verbose_name='Подпись')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Фотография детского сада'
        verbose_name_plural = 'Фотографии детских садов'

    def __str__(self):
        return f"Фото {self.kindergarten.name}"


class Kindergarten(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    address = models.CharField(max_length=300, verbose_name='Адрес')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    capacity = models.IntegerField(verbose_name='Вместимость', validators=[MinValueValidator(1)])
    established_at = models.DateField(verbose_name='Дата основания')
    
    # Новые поля
    description = models.TextField(blank=True, verbose_name='Описание')
    features = models.TextField(
        blank=True, 
        verbose_name='Особенности',
        help_text='Каждая особенность с новой строки'
    )
    is_recommended = models.BooleanField(default=False, verbose_name='Рекомендуемый')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Детский сад'
        verbose_name_plural = 'Детские сады'

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        rating = self.review_set.aggregate(Avg('rating'))['rating__avg']
        return rating if rating else 0

    @property
    def features_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]

    @property
    def group_count(self):
        return self.group_set.count()

    @property
    def teacher_count(self):
        return self.kindergartenteacher_set.count()


# Остальные модели остаются без изменений...
class Teacher(models.Model):
    QUALIFICATION_CHOICES = [
        ('высшая', 'Высшая категория'),
        ('первая', 'Первая категория'),
        ('вторая', 'Вторая категория'),
        ('без', 'Без категории'),
        ('молодой', 'Молодой специалист'),
    ]
    
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=20, verbose_name='Телефон')
    qualification = models.CharField(max_length=50, choices=QUALIFICATION_CHOICES, verbose_name='Квалификация')
    experience_years = models.IntegerField(default=0, verbose_name='Стаж (лет)')
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Воспитатель'
        verbose_name_plural = 'Воспитатели'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class KindergartenTeacher(models.Model):
    ROLE_CHOICES = [
        ('воспитатель', 'Воспитатель'),
        ('старший', 'Старший воспитатель'),
        ('методист', 'Методист'),
        ('заведующий', 'Заведующий'),
        ('психолог', 'Психолог'),
        ('логопед', 'Логопед'),
    ]
    
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Воспитатель')
    kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE, verbose_name='Детский сад')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='воспитатель', verbose_name='Должность')
    years_at_kindergarten = models.IntegerField(default=0, verbose_name='Стаж в этом саду (лет)')
    
    class Meta:
        unique_together = ['teacher', 'kindergarten']
        verbose_name = 'Работа воспитателя в саду'
        verbose_name_plural = 'Работы воспитателей в садах'

    def __str__(self):
        return f"{self.teacher} в {self.kindergarten}"


class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название группы')
    kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE, verbose_name='Детский сад')
    age_range = models.CharField(max_length=50, verbose_name='Возрастная группа')
    max_capacity = models.IntegerField(default=15, verbose_name='Максимальная вместимость')
    
    class Meta:
        ordering = ['kindergarten', 'name']
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return f"{self.name} ({self.kindergarten.name})"


class Child(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    birth_date = models.DateField(verbose_name='Дата рождения')
    parent_contact = models.CharField(max_length=100, verbose_name='Контакты родителей')
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Ребенок'
        verbose_name_plural = 'Дети'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('активна', 'Активна'),
        ('ожидание', 'В ожидании'),
        ('отклонена', 'Отклонена'),
        ('завершена', 'Завершена'),
    ]
    
    child = models.ForeignKey(Child, on_delete=models.CASCADE, verbose_name='Ребенок')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    enrollment_date = models.DateField(auto_now_add=True, verbose_name='Дата записи')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ожидание', verbose_name='Статус')
    
    class Meta:
        unique_together = ['child', 'group']
        verbose_name = 'Запись в группу'
        verbose_name_plural = 'Записи в группы'

    def __str__(self):
        return f"{self.child} в {self.group}"


class Review(models.Model):
    kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE, verbose_name='Детский сад')
    parent_name = models.CharField(max_length=100, verbose_name='Имя родителя')
    parent_email = models.EmailField(blank=True, verbose_name='Email родителя')
    parent_phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон родителя')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        verbose_name='Оценка'
    )
    comment = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"Отзыв от {self.parent_name} о {self.kindergarten.name}"

 