from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        

class UserProfileSerializer(serializers.ModelSerializer):
    #serialize nested user model
    user = UserSerializer(required=False)

    class Meta:
        model = UserProfile
        fields = ['user', 'credit_card', 'address', 'mobile']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        # Update UserProfile fields
        instance.credit_card = validated_data.get('credit_card', instance.credit_card)
        instance.address = validated_data.get('address', instance.address)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.save()

        # Update the nested User fields
        if user_data:
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.save()

        return instance