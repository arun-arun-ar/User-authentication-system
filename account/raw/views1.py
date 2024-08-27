from django.shortcuts import render, redirect
from django.http import HttpResponse
from models import UsersTable
from django.contrib.auth.hashers import make_password, check_password
import random
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
import re

# Create your views here.


# Getting random Number String
print(random.random())
randNum = random.random()
randNumString = str(randNum)
randWholeNumString = randNumString.split('.')[1]
print(randNum,randNumString,randWholeNumString)


def get_random_token():
    randNum = random.random()
    randNumString = str(randNum)
    randWholeNumString = randNumString.split('.')[1]
    return randWholeNumString

def send_welcome_email(request, userObj):
    try:
        # Welcome Email
        subject = "Welcome to authentication system!!"
        message ="""
        Welcome !!!
        """
        from_email = settings.EMAIL_HOST_USER
        to_list = [userObj.email,]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        return True
    except:
        pass

def send_confirmation_email(request, userObj):
    try:
        # Welcome Email
        subject = "Welcome to authentication system!!"
        current_site = get_current_site(request)
        domain_name = current_site.domain
        link = f'http://{domain_name}/verify/{userObj.token}'
        message = f'Hello, please click  link to confirm your registration : {link} '        
        
        from_email = settings.EMAIL_HOST_USER
        to_list = [userObj.email,]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        return True
    except:
        pass

def regexValid(regex, data):
    try:
        if (re.search(regex, fname)):
            return True;
    except Exception as ex:
        print(ex)

def checkPassword(password):
    pswdCriterian = {
    "length_criteria":".{8,}",
    "lowercase_criteria":"[a-z]+",
    "uppercase_criteria":"[A-Z]+",
    "number_criteria":"[0-9]+",
    "symbol_criteria":"[^A-Za-z0-9]+", # her ^ => not
    }
    meetCriterian = True
    pswdErrors = {}
    if not regexValid(pswdCriterian["length_criteria"], password):
        pswdErrors["lengthError"] = "Password must have more then 8 characters!"
        meetCriterian = False
    if not regexValid(pswdCriterian["lowercase_criteria"], password):
        pswdErrors["lcaseError"] = "Password must have a lowercase character!"
        meetCriterian = False
    if not regexValid(pswdCriterian["uppercase_criteria"], password):
        pswdErrors["ucaseError"] = "Password must have a uppercase character!"
        meetCriterian = False
    if not regexValid(pswdCriterian["number_criteria"], password):
        pswdErrors["ucaseError"] = "Password must have a number !"
        meetCriterian = False
    if not regexValid(pswdCriterian["symbol_criteria"], password):
        pswdErrors["ucaseError"] = "Password must have a symbol !"
        meetCriterian = False
    
    result = {
        "flag" : meetCriterian,
        "errors" : pswdErrors
    }

    return result

def validateSignUpForm(request):
    try: 
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        email = request.POST['email']
        pswd = request.POST['pswd']
        cpswd = request.POST['cpswd']

            # Defining Regex
        nameRegex = "^[a-zA-Z]{2,20}$"
        unameRegex = "^\w{3,15}$"
        emailRegex = "^\w+\.*\w@[a-z]{3,20}\.[a-z]{2,4}"

        isValid = True;     
        formErrors = {}      
        if not regexValid(nameRegex, fname):
            isValid = False
            ['formErrors'] = "Please enter valid first name!"
        
        if not regexValid(nameRegex, lname):
            isValid = False
            formErrors['lnameError'] = "Please enter valid last name!"
        
        if not regexValid(unameRegex, uname):
            isValid = False
            formErrors['unameError'] = "Please enter valid username!"
        
        if not regexValid(emailRegex, email):
            isValid = False
            formErrors['emailError'] = "Please enter valid email!"

        checkPassword = checkPassword(pswd)

        if not checkPassword['flag']:
            isValid = False
            formErrors['pswdError'] = checkPassword['errors']

        result = {
            "flag": isValid,
            "errors": formErrors
        }

        return result

    except Exception as e:
        print(e)
        pass


def signup(request):
    try:
        # pass
        if request.method == "POST":
            # Ensuring form submission and it's request method to be post
            if "register_button" in request.POST:
                #to check register_button named button (which is supposed to be triggered for signup form) exists in post request created
                fname = request.POST['fname']
                lname = request.POST['lname']
                uname = request.POST['uname']
                email = request.POST['email']
                pswd = request.POST['pswd']
                cpswd = request.POST['cpswd']

                    # Form Validation
                
                formData = {
                    "fname": fname,
                    "lname": lname,
                    "uname": uname,
                    "email": email,
                }

                isFormValid = True;

                formCheck = validateSignUpForm(request)

                if not formCheck["flag"]:
                    isFormValid = False

                if isFormValid:
                    if UsersTable.objects.filter(username = uname):
                        print("Username taken!")
                    if UsersTable.objects.filter(email = email):
                        print("Email is already registered!")
                    # userObj = UsersTable(first_name=fname, last_name=lname, username=uname, email=email, password=pswd)
                    hash_pswd = make_password(pswd)
                    userObj = UsersTable(first_name=fname, last_name=lname, username=uname, email=email, password=hash_pswd)
                    # UserObj is an instance of UsersTable model (since it is class) is created where we pass and assign form field value to corresponding field in database.
                    token = get_random_token()
                    userObj.token = token
                    userObj.save()
                    if send_welcome_email(request, userObj):
                        print("Sent!!")
                    else:
                        print("Not Sent!!")
                    if send_confirmation_email(request, userObj):
                        print("C Sent!!")
                    else:
                        print("C Not Sent!!")

                    templatePath = "account/signup.html"
                    context = {
                        "isRegistered": True
                    }
                    response = render(request, templatePath, context)
                    return response
                else:
                    templatePath = "account/signup.html"
                    context = {
                        "formErrors": formCheck['errors'],
                        "formData" : formData
                    }
                    response = render(request, templatePath, context)
                
    except Exception as e:
        print(e)
        pass
    templatePath = "account/signup.html"
    context = {}
    response = render(request, templatePath, context)
    return response

def login(request):
    try:
        pass
        if request.method == "POST":
            if "login_button" in request.POST:
                uname = request.POST['uname']
                pswd = request.POST['pswd']
                user = UsersTable.objects.filter(username = uname)


                if user:
                    password = user[0].password
                    isVerified = user[0].is_verified
                    # print(password)
                    passFlag = check_password(pswd, password)
                    verifyFlag = False
                    if isVerified:
                        verifyFlag = True
                    if passFlag and verifyFlag:
                        print("Success!")
                        request.session['user'] = user[0].id
                        request.session['email'] = user[0].email
                        request.session['username'] = user[0].username
                        return redirect('index')

                    else:
                        print("Can't Login!")
                        print("Verify email!")
                else:
                    print("Username or Email do not exist!")


    except Exception as e:
        print(e)
        pass   
    templatePath = "account/login.html"
    context = {}
    response = render(request, templatePath, context)
    return response

def verify(request, token):
    user = UsersTable.objects.filter(token=token)
    if user:
        print("Verified!")
        temp = user[0]
            # Since user is a query set !
        temp.is_verified = True
        temp.save()
        # user.save()
        templatePath = "account/verify.html"
        context = {
            "verifyFlag": True,
            "msg": "Verification Success!"
        }
        response = render(request, templatePath, context)
        return response
    templatePath = "account/verify.html"
    context = {
        "verifyFlag": False,
        "msg": "Verification failed!"
    }
    response = render(request, templatePath, context)
    return response

def profile(request):
    context = {}
    try:
        session = request.session
        if session['username']:
            userObj = UsersTable.objects.filter(username = session['username'])
            print(userObj)
            context = {
                "isAuthenticated": True,
                "userData": {
                    "fname": userObj[0].first_name,
                    "lname": userObj[0].last_name,
                    "username": userObj[0].username,
                    "email": userObj[0].email,
                }
            }
            templatePath = "account/profile.html"
    except Exception as e:
        print(e)
        templatePath = "404.html"
    response = render(request, templatePath, context)
    return response

def logout(request):
    request.session.clear()
    return redirect('index')