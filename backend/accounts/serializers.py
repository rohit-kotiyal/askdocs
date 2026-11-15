from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from .models import Organization, User



class RegisterSerializer(serializers.Serializer):
    organization_name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[validate_password])


    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        org = Organization.objects.create(name=validated_data["organization_name"])
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            organization=org,
            role=User.Role.ADMIN,
        )