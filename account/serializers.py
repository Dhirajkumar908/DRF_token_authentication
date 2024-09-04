from rest_framework import serializers 
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

class UserLoginSerializer(serializers.ModelSerializer):
    id=serializers.PrimaryKeyRelatedField(read_only=True)
    username=serializers.CharField(read_only=True)
    password=serializers.CharField(read_only=True)

    class Meta:
        model=User
        fields = ['id', 'username', 'password']

class UserRagistrationSerializer(serializers.ModelSerializer):
    id=serializers.PrimaryKeyRelatedField(read_only=True)
    username=serializers.CharField()
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['id', 'username', 'first_name', 'last_name','email', 'password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def Validate_username(self, username):
        if User.objects.filter(username=username).exists():
            details={'details':'User already exits'}
            raise ValidationError(detail=details)
        return username
    
    def validate(self,instance):
        if instance['password'] != instance['password2']:
            raise ValidationError({'message':'Both password must match'})
        if User.objects.filter(email=instance['email']).exists():
            raise ValidationError({'message':'Email already exist'})
        return instance
    
    def create(self, validated_data):
        password=validated_data.pop('password')
       
        user=User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            )
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user
        
    