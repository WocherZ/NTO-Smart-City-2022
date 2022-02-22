from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    )


class Analysis(models.Model):
    name = models.CharField(
        verbose_name="Название анализа",
        max_length=32,
    )
    value = models.TextField(
        verbose_name="Значение анализа",
    )

    patient = models.ForeignKey(
        'Patient',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Пациент котрому принадлежит анализ",
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Анализ"
        verbose_name_plural = "Список анализов"



class Patient(models.Model):
    first_name = models.CharField(
        verbose_name="Имя пациента",
        max_length=32,
    )
    last_name = models.CharField(
        verbose_name="Фамилия пациента",
        max_length=32,
    )
    login = models.CharField(
        verbose_name="Логин пациента",
        max_length=16,
    )
    password = models.CharField(
        verbose_name="Пароль пациента",
        max_length=16,
    )
    gender = models.CharField(
        verbose_name="Пол",
        max_length=1,
        choices=GENDER_CHOICES
    )
    # Базовые параметры пациента
    age = models.IntegerField(
        verbose_name="Возраст",
        validators=[
            MaxValueValidator(200),
            MinValueValidator(0)
        ],
        null=True,
    )
    weight = models.FloatField(
        verbose_name="Вес",
        null=True
    )
    height = models.FloatField(
        verbose_name="Рост",
        null=True
    )

    diagnosis = models.CharField(
        verbose_name="Заболевание пациента",
        null=True,
        max_length=32
    )

    room = models.ForeignKey(
        'Room',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Комната пациента",
    )

    doctor = models.ForeignKey(
        'Doctor',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Лечащий доктор",
    )

    image_link = models.CharField(
        verbose_name="Ссылка на картинку пациента",
        max_length=16,
        null=True,
        blank=True
    )

    def get_absolute_url(self):
        return f'/patient/{self.id}'

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Список пациентов"


class Room(models.Model):
    temperature = models.FloatField(
        verbose_name="Текущая температура",
    )
    illumination = models.IntegerField(
        verbose_name="Освещённость",
        validators=[
            MaxValueValidator(1023),
            MinValueValidator(0)
        ]
    )
    fan = models.IntegerField(
        verbose_name="Мощность вентилятора",
        validators=[
            MaxValueValidator(255),
            MinValueValidator(0)
        ]
    )
    heater = models.IntegerField(
        verbose_name="Нагреватель",
        validators=[
            MaxValueValidator(255),
            MinValueValidator(0)
        ],
        null=True
    )
    humidity = models.IntegerField(
        verbose_name="Уровень влажности",
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ],
        null=True
    )
    door = models.BooleanField(
        verbose_name="Дверь в комнате",
    )
    window = models.BooleanField(
        verbose_name="Окно в комнате",
    )

    is_present = models.BooleanField(
        verbose_name="Присутствие в комнате",
        null=True
    )

    def get_absolute_url(self):
        return f'/room/{self.id}'

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"



class Doctor(models.Model):
    first_name = models.CharField(
        verbose_name="Имя врача",
        max_length=32,
    )
    last_name = models.CharField(
        verbose_name="Фамилия врача",
        max_length=32,
    )
    login = models.CharField(
        verbose_name="Логин врача",
        max_length=16,
    )
    password = models.CharField(
        verbose_name="Пароль врача",
        max_length=16,
    )
    gender = models.CharField(
        verbose_name="Пол",
        max_length=1,
        choices=GENDER_CHOICES
    )
    profession = models.CharField(
        verbose_name="Должность врача",
        max_length=16,
        null=True
    )
    age = models.IntegerField(
        verbose_name="Возраст",
        validators=[
            MaxValueValidator(200),
            MinValueValidator(0)
        ],
        null=True
    )
    email = models.EmailField(
        verbose_name="Почта врача",
        null=True,
    )

    image_link = models.CharField(
        verbose_name="Ссылка на картинку врача",
        max_length=16,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Список врачей"

