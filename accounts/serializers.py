from rest_framework import serializers
from . models import CustomUser
import re


class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = CustomUser
    fields = ('id', 'username', 'email', 'profile_image',)


class RegisterSerializer(serializers.ModelSerializer):
  error_messages = {
    'invalid_email': 'That email address is not valid, please enter a valid email address',
    'username_rules': "User name must not contain any special character aside from space.",
    'valid_images': "Image uploaded is not in valid form, must be in png or jpg format!",
    'file_size_exceeded': "File size exceeded, please upload an image whose size is less than 1 MB."
  }

  class Meta:
    model = CustomUser
    fields = ('id', 'username', 'email', 'password', 'profile_image',)
    extra_kwargs = {'password': {'write_only': True}, 'profile_image': {'required': False}}

  def validate_username(self, value):
    pattern = '^[^0-9][a-zA-Z0-9_ ]+$'
    result = re.match(pattern, value)

    if value and not result:
      raise serializers.ValidationError(
        self.error_messages['username_rules'],
        code='username_rules'
      )
    return value

  def validate_email(self, value):
    # for validating an Email
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, value):
      raise serializers.ValidationError(
        self.error_messages['invalid_email'],
        code='invalid_email'
      )
    return value

  def validate_profile_image(self, value):
    if value:
      if value.size > 1048576:
        raise serializers.ValidationError(
          self.error_messages['file_size_exceeded'],
          code='file_size_exceeded'
        )
      return value
    else:
      pass






