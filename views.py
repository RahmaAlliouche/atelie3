from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render,HttpResponse

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse


from rest_framework import status

from rest_framework import authentication, permissions
from rest_framework.generics import ListAPIView

@api_view(['GET','DELET','ADD'])
def responce(request):
    return HttpResponse('Hello world')
    

from rest_framework.exceptions import AuthenticationFailed
from .serialization import PatSerializer
from .serialization import DrivSerializer
from .serialization import MedSerializer
from .serialization import InferSerializer

from .models import User
import jwt, datetime
from .models import Patient
from .models import Medecine
from .models import Infermier
from .models import Driver

class RegisterView(APIView):
    def post(self, request):
        serializer = PatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = Driver.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
    


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = PatSerializer(user)
        return Response(serializer.data)
    


from django.shortcuts import render, redirect
from .models import Patient, Request, Medecine
from django.contrib.auth.decorators import login_required

from .forms import RequestForm



from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import Patient, Request, Medecine

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='/login')

def add_request(request, patient_id):
    try:
        patient = Patient.objects.get(pk=patient_id)
    except Patient.DoesNotExist:
        return HttpResponse("Patient not found.", status=404)
    
    SPECIALITES = ['Cardiologue', 'Dermatologue', 'Gynécologue', 'Ophtalmologue', 'Orthopédiste']
    
    if request.method == 'POST':
        # handle form submission
        date = request.POST.get('date')
        time = request.POST.get('time')
        specialite = request.POST.get('specialite')
        # create new request object and save it
        request_obj = Request(patient=patient, requester=patient, date=date, time=time, specialite=specialite)
        request_obj.save()
        return redirect('patient_detail', patient_id=patient_id)
    else:
        # display form to user
        return render(request, 'add_request.html', {'patient': patient, 'SPECIALITES': SPECIALITES})

from django.shortcuts import render, get_object_or_404
from .models import Patient

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    # do something with the patient object
    return render(request, 'patient_detail.html', {'patient': patient})


#CANCEL VIEW

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def cancel_request(request, request_id):
    request_obj = Request.objects.get(pk=request_id)
    if request.user == request_obj.requester:
        request_obj.is_cancelled = True
        request_obj.save()
    return redirect('patient_detail', patient_id=request_obj.patient.id)

from django.shortcuts import render
from django.contrib.auth import authenticate, login

from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt




from django.shortcuts import render
from django.http import JsonResponse

from django.contrib.auth.hashers import check_password

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Administrator

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Administrator



from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
from .models import User

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .models import User

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                if user.is_admin:
                    # Successful authentication
                    login(request, user)
                    return redirect(Admin_view)
                else:
                    # User is not an admin
                    return render(request, 'login.html', {'error': 'You do not have permission to access the admin area.'})
            else:
                # Invalid credentials
                return render(request, 'login.html', {'error': 'Invalid credentials'})
        except User.DoesNotExist:
            # User does not exist
            return render(request, 'login.html', {'error': 'User does not exist'})
    else:
        return render(request, 'login.html')


from django.shortcuts import render

def Admin_view(request):
    return render(request, 'Home.html')

def show_all_doctors(request):
    doctors = Medecine.objects.all()
    return render(request, 'staff/doctor_list.html', {'doctors': doctors})

from django.shortcuts import render
from .models import Infermier


def nurse_list(request):
    nurses = Infermier.objects.all()
    return render(request, 'staff/nurse_list.html', {'nurses': nurses})

def driver_list(request):
    drivers = Driver.objects.all()
    return render(request, 'staff/driver_list.html', {'drivers': drivers})


from django.shortcuts import render
from .models import Patient

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'staff/Menu.html', {'patients': patients})


def add_doctor(request):
    if request.method == 'POST':
        name = request.POST['name']
        prenom = request.POST['prenom']
        email = request.POST['email']
        adress = request.POST['adress']
        spécialité = request.POST['spécialité']
        doctor = Medecine(name=name, prenom=prenom, email=email, adress=adress, spécialité=spécialité)
        doctor.save()
        return redirect('doctor_list')
    return render(request, 'staff/AddDoctor.html')



def show_all_request(request):
    requests = Request.objects.all()
    return render(request, 'request.html', {'requests': requests})
