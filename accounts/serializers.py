from rest_framework import serializers

from . import models


class UserRegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=13)
    short_info = serializers.CharField()
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ['username', 'password', 'password2', 'profile_image', 'phone_number', 'short_info']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Пароли не совпадают')
        return data

    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError('Пароль должен быть длиннее 8 символов')
        if not any(value.isdigit() for value in password):
            raise serializers.ValidationError('В пароле должны присутсвовать цифры')
        if not any(value.isupper() for value in password):
            raise serializers.ValidationError('В пароле должны быть заглавные буквы')
        if not any(value.islower() for value in password):
            raise serializers.ValidationError('В пароле должны быть прописные буквы')
        if not any(value in '!@#$%^&*()_-[]{}<>' for value in password):
            raise serializers.ValidationError('В пароле должны быть спецсимволы')
        return password

    def create(self, validated_data):
        user = models.User(
            username=validated_data['username'],
        )
        profile_image = validated_data.get('profile_image')
        if profile_image:
            user.profile_image = profile_image
        user.set_password(validated_data['password'])
        user.save()
        try:
            profile = models.Profile.objects.create(
                user=user,
                phone_number=validated_data['phone_number'],
                short_info=validated_data['short_info']
            )
        except Exception as e:
            user.delete()
            raise e
        else:
            profile.username = user.username
            profile.profile_image = user.profile_image
        return profile
