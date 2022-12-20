from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .models import *
import re
#from verify_email.email_handler import send_verification_email         #for sending email from signup form

# Create your views here.

def login(request) :
    return render(request, 'login.html')


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
        mobileFromAadhaar = data.get('check')
        mobile = data.get('mobile')
        email = data.get('email')
        pin = data.get('pin')
        confirm_pin = data.get('confirm_pin')

        values = {
            'aadhaar': aadhaar,
            'username': username,
            'mobileFromAadhaar': mobileFromAadhaar,
            'mobile': mobile,
            'email': email
        }

        #aadhaar validation....
        #c1 : not entered or invalid length
        if not aadhaar or len(aadhaar) != 12 :
            errorMessage = 'Aadhaar number should be 12-digit long'
        #c2 : aadhaar number does not exist
        found = False
        mob = None
        for obj in details.iterator():
            if obj.AadhaarNum == aadhaar :
                found = True
                mob = obj.Mobile
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
        if mobileFromAadhaar :
            mobile = mob
        else:
            if not mobile or len(mobile) != 10 :
                errorMessage = 'Mobile number should be 10 digit long'

        if errorMessage:
            return render(request, 'signup.html', {'error': errorMessage, 'val': values})

        #VALIDATION ENDS
                
        return HttpResponse('Success')