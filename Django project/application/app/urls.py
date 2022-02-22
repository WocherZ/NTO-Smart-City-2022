from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.rooms, name='rooms'),
    path('room/<int:room_id>/', views.room, name='room'),
    path('patients/', views.patients, name='patients'),
    path('patient/<int:patient_id>', views.patient, name='patient'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctor/<int:doctor_id>', views.doctor, name='doctor'),
    path('create_patient', views.create_patient, name='create_patient'),
    path('login', views.login, name='login'),
    path('profile', views.profile, name='profile'),
    path('registration', views.registration, name='registration'),
    path('data/', views.data, name='data'),
    path('logout', views.logout, name='logout'),
    path('create_analysis', views.create_analysis, name='create_analysis'),
    path('patient/<int:pk>/update/', views.UpdatePatient.as_view(), name='update_product'),
    path('room/<int:pk>/update/', views.UpdateRoom.as_view(), name='update_room'),

    path('temperature/', views.give_temperature),
    path('illumination/', views.give_illumination),
    path('fan/', views.give_fan),
    path('heater/', views.give_heater),
    path('humidity/', views.give_humidity),
    path('door/', views.give_door),
    path('window/', views.give_window),
    path('is_present/', views.give_is_present),
    path('weight/', views.give_weight),

    path('check_face/', views.check_face),

]
