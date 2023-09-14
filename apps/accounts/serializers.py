from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from apps.accounts.models import (
    User,
    Customer,
    Biller,
    Supplier,
)
from apps.store.serializers import WarehouseSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "phone",
            "email",
            "password",
            "password2",
            "gender",
            "username",
            "role",
        )

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {
                    "password": "The two password fields did not match"
                }
            )
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password2', None)
        user = User.objects.create(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()

        return user


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = (
            "id",
            "user",
            "supplier_code",
            "company",
        )


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "id",
            "user",
            "supplier_name",
            "customer_group",
            "reward_point",
        )


class BillerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biller
        fields = (
            "id",
            "user",
            "NID",
            "warehouse",
            "biller_code"
        )


class GetUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "phone",
            "email",
            "gender",
            "username",
        )


class GetSupplierSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Supplier
        fields = (
            "id",
            "user",
            "supplier_code",
            "company",
        )


class GetBillerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    modified_by = UserSerializer()
    warehouse = WarehouseSerializer()

    class Meta:
        model = Biller
        fields = (
            "id",
            "user",
            "modified_by",
            "biller_code",
            "NID",
            "warehouse",
            "country",
            "city",
            "street",
            "zip_code"
        )


class GetCustomerSerializer(serializers.ModelSerializer):
    supplier_name = GetSupplierSerializer()

    class Meta:
        model = Customer
        fields = (
            "supplier_name",
            "customer_group",
            "reward_point",
        )


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return value


    
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    
    class Meta:
        fields = ['email']

 
class ForgotPasswordSerializer(serializers.ModelSerializer):
    otp = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['otp', 'password', 'password1']
        
    def validate_otp(self, value):
        user = self.context['user']

        if user.otp != value:
            raise serializers.ValidationError("Sorry the otp doesn't match")
        return value
    
    def validate(self, data):
        if data.get('password') != data.get('password1'):
            raise serializers.ValidationError({'password' : 'password do not match'} )
        return data
    
    def update(self, instance, validated_data):
        instance.set_password(validate_password.get('password'))
        instance.save()
        return instance