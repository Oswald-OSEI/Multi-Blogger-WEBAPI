from rest_framework import serializers
from .models import Account, Profile, loginmodel

class AccountSerializer(serializers.ModelSerializer):
    password_again = serializers.CharField(style={"input_type": "password"})
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'password', 'password_again']
       

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'telephone_number', 'date_of_birth', 'about', 'Gender']

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = loginmodel
        fields = ["email", "password"]
        write_only_fields = ["password"]