from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication

from django.contrib.auth import get_user_model
from rest_auth.serializers import PasswordResetConfirmSerializer

from django.utils.http import urlsafe_base64_decode as uid_decoder
from rest_framework.exceptions import ValidationError
from django.utils.encoding import force_text


User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    # first_name last_name
    username = serializers.CharField(max_length=150, min_length=4, required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
        }

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass


# class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
#     new_password1 = serializers.CharField(max_length=128)
#     new_password2 = serializers.CharField(max_length=128)

#     def validate(self, attrs):
#         self._errors = {}

#         try:
#             uid = force_text(uid_decoder(attrs['uidb64']))
#             self.user = User._default_manager.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#                 raise ValidationError({'uid': ['Invalid value']})
#         return super().validate(attrs)
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    def validate(self, attrs):
        self._errors = {}

        try:
            uidb64 = self.context["request"].parser_context["kwargs"]["uidb64"]
            token = self.context["request"].parser_context["kwargs"]["token"]
            uid = force_text(urlsafe_base64_decode(uidb64))
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({"uid": ["Invac value"]})

        if not default_token_generator.check_token(self.user, token):
            raise ValidationError({"token": ["Invalid or expired token"]})

        attrs["new_password1"] = attrs["new_password1"].strip()
        attrs["new_password2"] = attrs["new_password2"].strip()

        return super().validate(attrs)
