from .models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('name','email','password')
        extra_kwargs={'password':{'write_only':True}}
    def create(self, validated_data):                                           #override customize create behaviour
        user=User(
            email=validated_data['email'],                                #validate user

        )
        user.set_password(validated_data['password'])                           #validate password
        user.save()
        Token.objects.create(user=user)                                         #create token for respective user.
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('email','password')

