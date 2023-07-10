from django.utils.encoding import force_text
from django.contrib.auth.forms import SetPasswordForm
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication

from rest_auth.serializers import UserDetailsSerializer
from rest_auth.registration.serializers import RegisterSerializer

from post.serializers import CommentSerializer 

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
    
    
    
class CustomUserDetailsSerializer(UserDetailsSerializer):
    comments = serializers.SerializerMethodField()
    
    def get_comments(self, obj):
        req = self.context.get('request')
        comments = obj.comments.filter(user=req.user)
        comments_seriallizer = CommentSerializer(comments, many=True)
        return comments_seriallizer.data
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep
    
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'comments')
        read_only_fields = ('email', )


class CustomPasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    
    set_password_form_class = SetPasswordForm

    def validate(self, attrs):
        self._errors = {}

        try:
            uidb64 = self.context["request"].parser_context["kwargs"]["uidb64"]
            token = self.context["request"].parser_context["kwargs"]["token"]
            uid = force_text(urlsafe_base64_decode(uidb64))
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({"uid": ["Invac value"]})
        
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        
        
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
       

        attrs["new_password1"] = attrs["new_password1"].strip()
        attrs["new_password2"] = attrs["new_password2"].strip()

        return super().validate(attrs)

    def save(self):
        return self.set_password_form.save()