from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        

class UserProfileSerializer(serializers.ModelSerializer):
    #not required if only profile data is updated
    user = UserSerializer(required=False)

    class Meta:
        model = UserProfile
        fields = ['user', 'credit_card', 'address', 'mobile']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if user_data:
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        return instance