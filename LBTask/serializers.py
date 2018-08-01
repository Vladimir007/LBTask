from rest_framework import serializers
from shop.models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'patronymic', 'group')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('is_staff', 'is_active', 'date_joined')
