from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from .forms import PatientForm, LoginForm, AnalysisForm, RegistrationForm
from .models import Patient, Doctor, Room, Analysis
from .user_registration import check_registration, login_required, doctor_permission


# Главная страница сайта
def home(request):
    context = {}
    if request.session.get('role') == 2:
        context['role'] = "Врач"
    if request.session.get('role') == 1:
        context['role'] = "Пациент"

    return render(request, 'home.html', context=context)


# Список комнат
@doctor_permission
def rooms(request):
    context = {}
    if request.session.get('role') == 2:
        context['role'] = "Врач"
    if request.session.get('role') == 1:
        context['role'] = "Пациент"

    info = []
    for room_object in Room.objects.all():
        info.append({
            'id': room_object.id
        })
    context['rooms'] = info
    return render(request, 'rooms.html', context=context)


# Страница комнаты
def room(request, room_id):
    context = {}
    if request.session.get('role') == 2:
        context['role'] = "Врач"
    if request.session.get('role') == 1:
        context['role'] = "Пациент"

    # Проверка что пользователь - врач
    if request.session.get('role') != 2:
        return HttpResponseForbidden()

    try:
        room_object = Room.objects.get(id=room_id)
        context['id'] = room_object.id
        context["temperature"] = room_object.temperature
        context["illumination"] = room_object.illumination
        context["fan"] = room_object.fan
        context["heater"] = room_object.heater
        context["humidity"] = room_object.humidity
        context["door"] = room_object.door
        context["window"] = room_object.window
        context["is_present"] = room_object.is_present
        context["link_update"] = "/room/" + str(context.get('id')) + "/update/"

    except ObjectDoesNotExist:
        raise Http404

    return render(request, 'room.html', context=context)


# Список пациентов
@doctor_permission
def patients(request):
    context = {}
    if request.session.get('role') == 2:
        context['role'] = "Врач"
    if request.session.get('role') == 1:
        context['role'] = "Пациент"

    info = []
    for patient_object in Patient.objects.all():
        info.append({
            'id': patient_object.id,
            'first_name': patient_object.first_name,
            'last_name': patient_object.last_name,
        })
    context['patients'] = info
    return render(request, 'patients.html', context=context)


# Страница пациента
def patient(request, patient_id):
    context = {}
    if request.session.get('role') == 2:
        context['role'] = "Врач"
    if request.session.get('role') == 1:
        context['role'] = "Пациент"

    # Проверка что пользователь - врач
    if request.session.get('role') != 2:
        return HttpResponseForbidden()

    try:
        patient_object = Patient.objects.get(id=patient_id)
        context['id'] = patient_object.id
        context['first_name'] = patient_object.first_name
        context['last_name'] = patient_object.last_name
        context['gender'] = patient_object.gender
        context['age'] = patient_object.age
        context['weight'] = patient_object.weight
        context['height'] = patient_object.height
        context['diagnosis'] = patient_object.diagnosis
        context['link_update'] = "/patient/" + str(context.get('id')) + "/update/"

    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'patient.html', context=context)


# Список врачей
@login_required
def doctors(request):
    context = {}
    if request.session.get('role') == 2:
        context['role'] = "Врач"
    if request.session.get('role') == 1:
        context['role'] = "Пациент"

    info = []
    for doctor_object in Doctor.objects.all():
        info.append({
            'id': doctor_object.id,
            'first_name': doctor_object.first_name,
            'last_name': doctor_object.last_name,
        })
    context['doctors'] = info
    return render(request, 'doctors.html', context=context)


# Страница врача
def doctor(request, doctor_id):
    context = {}
    if request.session.get('role') == 2:
        context['role'] = "Врач"
    if request.session.get('role') == 1:
        context['role'] = "Пациент"

    # Проверка на авторизованного пользователя
    if request.session.get('role') is None:
        return HttpResponseForbidden()

    try:
        doctor_object = Doctor.objects.get(id=doctor_id)
        context['id'] = doctor_object.id
        context['first_name'] = doctor_object.first_name
        context['last_name'] = doctor_object.last_name
        context['gender'] = doctor_object.gender
        context['age'] = doctor_object.age
        context['email'] = doctor_object.email
        context['profession'] = doctor_object.profession
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'doctor.html', context=context)


# Вход в систему
def login(request):
    context = {}
    if request.session.get('role') == 2:
        context['role'] = "Врач"
    if request.session.get('role') == 1:
        context['role'] = "Пациент"

    if request.method == 'POST':
        print("Попытка входа")
        form = LoginForm(request.POST)

        if form.is_valid():
            user_login = form.cleaned_data['login']
            user_password = form.cleaned_data['password']
            user = Patient.objects.filter(login=user_login).filter(password=user_password)
            if user.first():  # Такой пациент нашёлся
                print("Успешный вход пользователя - пациента")
                request.session['is_login'] = True
                request.session['role'] = 1
                request.session['user_id'] = user.first().id
                return redirect('profile')
            else:
                user = Doctor.objects.filter(login=user_login).filter(password=user_password)
                if user.first():  # Такой врач нашёлся
                    print("Успешный вход пользователя - врача")
                    request.session['is_login'] = True
                    request.session['role'] = 2
                    request.session['user_id'] = user.first().id
                    return redirect('profile')

                print("Пользователь не смог войти - не найден такой логин")
                context['error'] = "Введены неверные данные"
                context['form'] = LoginForm()
                return render(request, 'login.html', context)

    else:
        form = LoginForm()

    context['form'] = form
    return render(request, 'login.html', context)


# Добавление нового пациента
@doctor_permission
def create_patient(request):
    context = {}
    if request.session.get('role') == 2:
        context['role'] = "Врач"
    if request.session.get('role') == 1:
        context['role'] = "Пациент"

    error = ''
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()

            context['form'] = form
            context['error'] = "Пациент успешно создан"
            return render(request, "create_patient.html", context=context)
        else:
            error = "Форма неверно заполнена"

    form = PatientForm()

    context['form'] = form
    context['error'] = error

    return render(request, "create_patient.html", context=context)


# Страница личного кабинета
@login_required
def profile(request):
    context = {}
    if request.session.get('role') == 2:
        context['role'] = "Врач"
    if request.session.get('role') == 1:
        context['role'] = "Пациент"

    if request.session.get('is_login'):
        if request.session.get('role') == 1:  # Паицент
            user_id = request.session.get('user_id')
            user = Patient.objects.get(id=user_id)
            context['first_name'] = user.first_name
            context['last_name'] = user.last_name
            context['doctor'] = str(user.doctor.last_name) + " " + str(user.doctor.first_name)
            context['doctor_id'] = user.doctor.id
            context['image_link'] = user.image_link
            context['diagnosis'] = user.diagnosis

            # Формирование списка анализов пациента
            context['analyzes'] = []
            analyzes = Analysis.objects.all()
            for analysis in analyzes:
                if analysis.patient.id == user_id:
                    context['analyzes'].append({
                        'name': analysis.name,
                        'value': analysis.value
                    })

        if request.session.get('role') == 2:  # Врач
            user_id = request.session.get('user_id')
            user = Doctor.objects.get(id=user_id)
            context['first_name'] = user.first_name
            context['last_name'] = user.last_name
            context['image_link'] = user.image_link
            context['profession'] = user.profession

            # Формирование списка пациентов врача
            context['patients'] = []
            for patient_object in Patient.objects.all():
                doc = patient_object.doctor
                if doc:
                    if doc.id == user_id:
                        context['patients'].append({
                            'patient_id': patient_object.id,
                            'first_name': patient_object.first_name,
                            'last_name': patient_object.last_name
                        })

        return render(request, "profile.html", context=context)
    else:
        pass
    return render(request, "profile.html", context=context)


# Регистрация
def registration(request):
    context = {}
    if request.session.get('role') == 2:
        context['role'] = "Врач"
    if request.session.get('role') == 1:
        context['role'] = "Пациент"

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user_login = form.cleaned_data['login']
            user_password = form.cleaned_data['password']
            user_first_name = form.cleaned_data['first_name']
            user_last_name = form.cleaned_data['last_name']
            if form.cleaned_data['gender'] == "M":
                user_gender = "М"
            else:
                user_gender = "Ж"
            user_age = form.cleaned_data['age']
            user_weight = form.cleaned_data['weight']
            user_height = form.cleaned_data['height']

            if check_registration(user_login) == 0:
                print("Пациент")
                user = Patient(login=user_login,
                               password=user_password,
                               first_name=user_first_name,
                               last_name=user_last_name,
                               gender=user_gender,
                               age=user_age,
                               weight=user_weight,
                               height=user_height
                               )
                user.save()
                context['error'] = "Пользователь успешно создан"
            else:
                context['error'] = "Уже существует пользователь с таким логином"

    context['form'] = RegistrationForm()
    return render(request, "registration.html", context=context)


# Выход пользователя из системы
def logout(request):
    del request.session['role']
    del request.session['user_id']
    request.session['is_login'] = False
    return redirect('home')


# Создание анализа пациента
@doctor_permission
def create_analysis(request):
    context = {}
    if request.session.get('role') == 2:
        context['role'] = "Врач"
    if request.session.get('role') == 1:
        context['role'] = "Пациент"

    error = ''
    if request.method == "POST":
        form = AnalysisForm(request.POST)
        if form.is_valid():
            form.save()

            context['form'] = form
            context['error'] = "Анализ сохранён"
            return render(request, "create_analysis.html", context=context)
        else:
            error = "Форма неверно заполнена"

    form = AnalysisForm()

    context['form'] = form
    context['error'] = error

    return render(request, "create_analysis.html", context=context)


class UpdatePatient(UpdateView):
    model = Patient
    template_name = "update_patient.html"

    fields = ["weight", "height", "diagnosis", "room", "doctor"]


class UpdateRoom(UpdateView):
    model = Room
    template_name = "update_room.html"

    fields = ['temperature', 'illumination', 'fan', 'heater', 'humidity', 'door', 'window', 'is_present']


GLOBAL_ROOM_ID = 1
GLOBAL_PATIENT_ID = 1


# Получение данных
def data(request):
    print("Пришёл запрос в data")

    temperature = request.GET.get("temperature")
    if temperature is not None:
        value = Room.objects.get(id=GLOBAL_ROOM_ID)
        value.temperature = temperature
        value.save()
    # print("Температура: " + str(temperature))

    illumination = request.GET.get("illumination")
    if illumination is not None:
        value = Room.objects.get(id=GLOBAL_ROOM_ID)
        value.illumination = illumination
        value.save()
    # print("Освещённость: " + str(illumination))

    fan = request.GET.get("fan")
    if fan is not None:
        value = Room.objects.get(id=GLOBAL_ROOM_ID)
        value.fan = fan
        value.save()
    # print("Вентилятор: " + str(fan))

    heater = request.GET.get("heater")
    if heater is not None:
        value = Room.objects.get(id=GLOBAL_ROOM_ID)
        value.heater = heater
        value.save()
    # print("Нагреватель: " + str(heater))

    humidity = request.GET.get("humidity")
    if humidity is not None:
        value = Room.objects.get(id=GLOBAL_ROOM_ID)
        value.humidity = humidity
        value.save()
    # print("Влажность: " + str(humidity))

    door = request.GET.get("door")
    if door is not None:
        value = Room.objects.get(id=GLOBAL_ROOM_ID)
        value.door = door
        value.save()
    # print("Дверь: " + str(door))

    window = request.GET.get("window")
    if window is not None:
        value = Room.objects.get(id=GLOBAL_ROOM_ID)
        value.window = window
        value.save()
    # print("Окно: " + str(window))

    is_present = request.GET.get("is_present")
    if is_present is not None:
        value = Room.objects.get(id=GLOBAL_ROOM_ID)
        value.is_present = is_present
        value.save()
    # print("Присутствие в комнате: " + str(is_present))

    weight = request.GET.get("weight")
    if weight is not None:
        value = Patient.objects.get(id=GLOBAL_ROOM_ID)
        value.weight = weight
        value.save()
    # print("Вес: " + str(weight))
    return HttpResponse("Успешно пришли данные от тебя")




def give_temperature(request):
    response = Room.objects.filter(id=GLOBAL_ROOM_ID).first().temperature
    print("Отправлено значение temperature")
    return HttpResponse(str(response))


def give_illumination(request):
    response = Room.objects.filter(id=GLOBAL_ROOM_ID).first().illumination
    print("Отправлено значение illumination")
    return HttpResponse(str(response))


def give_fan(request):
    response = Room.objects.filter(id=GLOBAL_ROOM_ID).first().fan
    print("Отправлено значение fan")
    return HttpResponse(str(response))


def give_heater(request):
    response = Room.objects.filter(id=GLOBAL_ROOM_ID).first().heater
    print("Отправлено значение heater")
    return HttpResponse(str(response))


def give_humidity(request):
    response = Room.objects.filter(id=GLOBAL_ROOM_ID).first().humidity
    print("Отправлено значение humidity")
    return HttpResponse(str(response))


def give_door(request):
    response = Room.objects.filter(id=GLOBAL_ROOM_ID).first().door
    print("Отправлено значение door")
    return HttpResponse(str(response))


def give_window(request):
    response = Room.objects.filter(id=GLOBAL_ROOM_ID).first().window
    print("Отправлено значение window")
    return HttpResponse(str(response))


def give_is_present(request):
    response = Room.objects.filter(id=GLOBAL_ROOM_ID).first().is_present
    print("Отправлено значение is_present")
    return HttpResponse(str(response))


def give_weight(request):
    response = Patient.objects.filter(id=GLOBAL_PATIENT_ID).first().weight
    print("Отправлено значение weight")
    return HttpResponse(str(response))



def check_face(request):
    value = Room.objects.get(id=GLOBAL_ROOM_ID)
    value.door = True
    value.save()
    print("Пришёл ответ от Face-ID")
    return HttpResponse("Success")
