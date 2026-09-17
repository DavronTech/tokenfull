from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User


class SignUpSerilazers(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'confirm_password',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Parollar bir xil emas'
            })

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            **validated_data
        )

        return user


class LoginSerilazers(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        username = attrs['username']
        password = attrs['password']

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                'Username yoki password noto‘g‘ri'
            )

        token, created = Token.objects.get_or_create(
            user=user
        )

        attrs['user'] = user
        attrs['token'] = token.key

        return attrs


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        ]
        read_only_fields = ['id', 'username']

    def validate(self, attrs):

        if attrs.get('first_name') == attrs.get('last_name'):
            raise serializers.ValidationError(
                'Ism va familiya bir xil bo‘lishi mumkin emas'
            )

        return attrs
    def validate_email(self, value):

        if value.endswith('@test.com'):
            raise serializers.ValidationError(
                'Bu emaildan foydalanish mumkin emas'
            )

        return value
    



class PasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField( write_only=True)

    def validate(self, attrs):

        user = self.context['request'].user

        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({
                'old_password': 'Eski parol noto‘g‘ri'
            })

        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Yangi parollar bir xil emas'
            })

        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({
                'new_password': 'Yangi parol eski paroldan farq qilishi kerak'
            })

        return attrs

    def save(self, **kwargs):

        user = self.context['request'].user

        user.set_password(self.validated_data['new_password'])

        user.save()

        return user


class LogoutSerializer(serializers.Serializer):

    def save(self, **kwargs):

        request = self.context['request']

        if request.auth:
            request.auth.delete()

        return True


