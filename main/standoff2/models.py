from django.db import models

class Child(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    birth_date = models.DateField(verbose_name="Дата рождения")
    parent_contact = models.CharField(max_length=255, verbose_name="Контакт родителя")

    def str(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Ребёнок"
        verbose_name_plural = "Дети"


class Teacher(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    qualification = models.CharField(max_length=255, verbose_name="Квалификация")

    def str(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Воспитатель"
        verbose_name_plural = "Воспитатели"


class Kindergarten(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    capacity = models.IntegerField(verbose_name="Вместимость (кол-во детей)")
    established_at = models.DateField(verbose_name="Дата основания")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    def str(self):
        return self.name

    class Meta:
        verbose_name = "Детский сад"
        verbose_name_plural = "Детские сады"


class Group(models.Model):
    kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE, verbose_name="Детский сад")
    name = models.CharField(max_length=255, verbose_name="Название группы")
    age_range = models.CharField(max_length=50, verbose_name="Возрастная категория")

    def str(self):
        return f"{self.name} ({self.kindergarten.name})"

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Enrollment(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, verbose_name="Ребёнок")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа")
    enrollment_date = models.DateField(verbose_name="Дата зачисления")
    status = models.CharField(max_length=255, verbose_name="Статус зачисления")

    def str(self):
        return f"Зачисление {self.id}: {self.child} в {self.group}"

    class Meta:
        verbose_name = "Зачисление"
        verbose_name_plural = "Зачисления"


class Review(models.Model):
    kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE, verbose_name="Детский сад")
    parent_name = models.CharField(max_length=255, verbose_name="Имя родителя")
    rating = models.IntegerField(verbose_name="Оценка (1–5)")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    def str(self):
        return f"Отзыв о {self.kindergarten} от {self.parent_name}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class KindergartenTeacher(models.Model):
    kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE, verbose_name="Детский сад")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Воспитатель")

    def str(self):
        return f"{self.teacher} — {self.kindergarten}"

    class Meta:
        verbose_name = "Связь детский сад–воспитатель"
        verbose_name_plural = "Связи детский сад–воспитатель"