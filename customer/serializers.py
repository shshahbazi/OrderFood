from rest_framework import serializers, exceptions

from .models import Profile, Address, Card


class AuthTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = Profile
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = None
        if email and password:
            user = Profile.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError("This email is not registered")
            if not user.check_password(password):
                raise serializers.ValidationError("Incorrect password")
        else:
            msg = ('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        data['user'] = user
        return data


class ProfileRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = (
            'password',
            'full_name',
            'email',)
        extra_kwargs = {'email': {'required': True}}

    def create(self, validated_data):
        user = Profile(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['picture']
