from django.shortcuts import render
from .serializers import AccountSerializer, ProfileSerializer, LoginSerializer
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from .models import Account, Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.
@api_view(['POST'])
def UserRegistration(request):
    if request.method == "POST":
        #if method is post, assign account to the inputted data(converted from JSON to Python objects by AccountSerializer)
        account = AccountSerializer(data = request.data)
        #check if the data is valid
        if account.is_valid(raise_exception = True):
            #get passwords from account(which is the inputted dat from the serializer)
            cd = account.data
            password1 = cd.get('password')
            password2 = cd.get('password_again')
            #compare both retrieved passwords
            if password1==password2:
                #if the passwords are the same, set password
                registered = Account.objects.create(
                    email = cd.get('email'), 
                    first_name = cd.get('first_name'), 
                    last_name = cd.get('last_name'), 
                )
                registered.set_password(password1)
                registered.save()
                your_profile = Profile.objects.create(account_holder = registered)
                your_profile.save()
                return Response('welcome')
            #if passwords don't match, notify the user that passwords don't match
            else:
                return Response('passwords do not match')
            
@api_view(["POST"])
def UserLogin(request):
    if request.method == "POST":
        logindata = LoginSerializer(data = request.data)
        if logindata.is_valid(raise_exception=True):
            cd = logindata.data
            authorise = authenticate(request, username = cd.get('email'), password = cd.get("password"))
            if authorise is not None:
                if authorise.is_active:
                    login(request, authorise)
                    return Response('login successful')
                else:
                    return Response("your account is not active")
            else:
                return Response("Your account Does not exist")
    #automatially check if user has a profile and if none, create a a profile for the user and if yes, get the profile of the user
   
            
        
@api_view(['GET'])
@login_required
def viewProfile(request):
    active_user = request.user
    try:
        current_profile = Profile.objects.get(account_holder = active_user)
    except ObjectDoesNotExist:
        current_profile = Profile.objects.create(account_holder = active_user)
        current_profile.save()
    your_profile = ProfileSerializer(current_profile).data
    return Response(your_profile)

@api_view(['GET', 'POST'])
@login_required
def editProfile(request):
    your_profile = Profile.objects.get(account_holder=request.user)
    updated_profile = ProfileSerializer(your_profile, data = request.data)
    if updated_profile.is_valid(raise_exception = True):
        updated_pic = request.FILES.get('profile_picture')
        if updated_pic is not None:
            updated_profile.profile_picture = updated_pic
            updated_profile.save()
        else:
            updated_profile.save()
        return Response(updated_profile.data)
    else:
        return Response("invalid update")
    
    

    
   
    
    

                





