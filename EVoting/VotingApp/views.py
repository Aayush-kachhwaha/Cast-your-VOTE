from django.shortcuts import redirect, render
from django.http import HttpResponse
from . import verify
from django.template import loader
from django.contrib import messages
from .models import *
import urllib
from .decorators import *
from django.contrib.auth.decorators import login_required

# Create your views here.


def verify_code(request):
    if request.method == 'GET' :
        return render(request, 'verify.html')
    else :
        data = request.POST
        otp = data.get('otp')
    
        errorMessage = None

        if not otp :
            errorMessage = "OTP is required for verification"

        if errorMessage :
            return render(request, 'verify.html')

        if verify.check(request.registeredUsers.mobile, otp):
                request.registeredUsers.mobile_verified = True
                request.registeredUsers.register()
                return HttpResponse('success otp')

        return HttpResponse('Failed')


def signup(request) :
    if request.method == 'GET' :
        return render(request, 'signup.html')

    else:
        data = request.POST   #taking form data filled by user
        details = aadhaarDB.objects.all()    #taking details from aadhaar db for validation
        errorMessage = None

        #VALIDATION STARTS
        aadhaar = data.get('aadhaar')
        username = data.get('username')
        mobile = data.get('mobile')
        pin = data.get('pin')
        confirm_pin = data.get('confirm_pin')

        values = {
            'aadhaar': aadhaar,
            'username': username,
            'mobile': mobile,
        }

        #aadhaar validation....
        #c1 : not entered or invalid length
        if not aadhaar or len(aadhaar) != 12 :
            errorMessage = 'Aadhaar number should be 12-digit long'
        #c2 : aadhaar number does not exist
        found = False
        age = 0
        for obj in details.iterator():
            if obj.AadhaarNum == aadhaar :
                age = obj.Age
                found = True
                break
        if(found == False):
            errorMessage = 'Aadhaar number is invalid, does not exist'
        #c3 : aadhaar number already present
        new = registeredUsers.objects.filter(aadhaar = aadhaar)
        if new.count() :
            errorMessage = 'Aadhaar number already registered with the portal'

        #username validation....
        #c1 : username not entered
        if not username :
            errorMessage = 'Username is required'
        #c2 : username already taken
        new = registeredUsers.objects.filter(username = username)
        if new.count():
            errorMessage = 'This username is already taken'

        #mobile validation
        mob = "+91"
        mobile = mob + mobile
        if not mobile or len(mobile) != 13 :
            errorMessage = "Mobile number ahould be 10 digit long"

        #pin validation
        #cond : pin not provided or length != 4
        if not pin :
            errorMessage = "Pin is required"
        elif len(pin) != 4:
            errorMessage = "Length of pin should be exactly 4"

        if not confirm_pin :
            errorMessage = "Confirm pin is required"
        elif confirm_pin != pin :
            errorMessage = "Confirm pin should be equal to pin"

        #age validation
        if age < 18 :
            errorMessage = "You are under-age. Minimum age to register and cast a vote is 18 years of age."

        #VALIDATION ENDS

        if errorMessage:
            return render(request, 'signup.html', {'error': errorMessage, 'val': values})
        else :
            user = registeredUsers(aadhaar = aadhaar,
                    username = username,
                    mobile = mobile,
                    pin = pin)
            user.register()              
            #verify.send(mobile)
            #return render(request, 'verify.html')
            #return redirect(verify_code)

            return redirect(login)


def login(request) :
    
    if request.method == 'GET' :
        return render(request, 'login.html')

    else:
        data = request.POST
        info = registeredUsers.objects.all()
        errorMessage = None

        username = data.get('username')
        pin = data.get('pin')
        confirm_pin = data.get('confirm_pin')

        p = ''

        if not username :
            errorMessage = "Username is required."

        else:
            found = False
            for obj in info.iterator() :
                if username == obj.username :
                    p = obj.pin
                    found = True
                    break

            if found == False :
                errorMessage = "Invalid username"

        if not pin :
            errorMessage = "Pin is required"
        elif pin != p :
            errorMessage = "Pin is not correct"

        if not confirm_pin :
            errorMessage = "Confirm pin is required"
        elif confirm_pin != pin :
            errorMessage = "Confirm pin should be same as the pin"

        if errorMessage :
            return render(request, 'login.html', {'error': errorMessage})
        
        else:
            return redirect(landing)


#@aadhaar_verification_required
#@login_required
def landing(request):
    if request.method == 'GET' :
        all = Election.objects.all()
        ongoing = []
        upcoming = []
        completed = []
        for obj in all.iterator():
            if str(obj.status) == 'Ongoing' :
                ongoing.append(obj)
            elif str(obj.status) == 'Upcoming' :
                upcoming.append(obj)
            else :
                completed.append(obj)
        
        return render(request, 'landing.html', {'ongoing' : ongoing, 'upcoming' : upcoming, 'completed' : completed})
    
    else :
        data = request.POST
        id = data.get('id')
        return redirect(vote, id=id)


def home(request):
    if request.method == 'GET' :
        all = Election.show_all()
        return render(request, 'home.html', {'all' : all})
    

def vote(request, id) :
    details = Election.objects.filter(id = id)
    return render(request, 'vote.html', {'details' : details})
    
    