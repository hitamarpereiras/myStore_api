from apps.accounts.models import User
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "telephone",
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Já existe um usuário com esse e-mail."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save(update_fields=["password"])

        return user

    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "telephone",
        )