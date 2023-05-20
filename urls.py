from django.urls import path
from . import views
from .views import RegisterView, driver_list, nurse_list, patient_list
from .views import LoginView
from .views import UserView
from .views import show_all_doctors

from .views import patient_detail


urlpatterns = [
    
    path('',views.responce),
    path('api/register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    #path('up/',views.signUp),
    path('patient/<int:patient_id>/request/add/', views.add_request, name='add_request'),
    path('request/<int:request_id>/cancel/', views.cancel_request, name='cancel_request'),
    path('patient/<int:patient_id>/', patient_detail, name='patient_detail'),
    path('log/', views.login, name='login'),
    
    path('admine/', views.Admin_view, name='Menu'),
    path('admine/doctors/', views.show_all_doctors,name='doctor_list'),
    path('admine/nurse/', views.nurse_list, name='nurse_list'),
    
    path('admine/driver/', views.driver_list, name='driver_list'),
    path('admine/pat/', views.patient_list, name='Menu'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('admine/requests/', views.show_all_request, name='show_all_request'),
    
  
]