from django.forms import ModelForm, TextInput, Textarea
from django import forms
from .models import Patient, Analysis

ROLE_CHOICE = (
    ("1", "Пациент"),
    ("2", "Врач"),
)

GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    )


class LoginForm(forms.Form):
    login = forms.CharField(label='Логин', max_length=32)
    password = forms.CharField(label='Пароль', max_length=32)


class RegistrationForm(forms.Form):
    login = forms.CharField(label='Логин', max_length=32)
    password = forms.CharField(label='Пароль', max_length=32)
    first_name = forms.CharField(label='Имя', max_length=32)
    last_name = forms.CharField(label='Фамилия', max_length=32)
    gender = forms.ChoiceField(label='Пол', choices=GENDER_CHOICES)
    age = forms.IntegerField(label='Возраст')
    weight = forms.FloatField(label='Текущий вес')
    height = forms.FloatField(label='Рост')


class AnalysisForm(ModelForm):
    class Meta:
        model = Analysis
        fields = [
            'name',
            'value',
            'patient'
        ]


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name',
                  'last_name',
                  'gender',
                  'age',
                  'weight',
                  'height',
                  'login',
                  'password',
                  'diagnosis',
                  'room',
                  'doctor'
                  ]

