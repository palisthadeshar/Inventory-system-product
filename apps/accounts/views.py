from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
)
from rest_framework.decorators import action
from apps.accounts.models import (
    User,
    Customer,
    Supplier,
    Biller,
)
from apps.accounts.serializers import (
    UserSerializer,
    SupplierSerializer,
    CustomerSerializer,
    BillerSerializer,
    GetSupplierSerializer,
    GetCustomerSerializer,
    GetBillerSerializer,
    GetUserListSerializer,
    ChangePasswordSerializer,
    EmailSerializer,
    ForgotPasswordSerializer,
)
from apps.store.serializers import WarehouseSerializer
from utils.pagination import MyPagination
from utils.emails import send_otp_email
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
import random
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import pyotp
from utils.permissions import CustomerPermssion


class CommonModelViewset(ModelViewSet):
    pagination_class = MyPagination


class UserViewSet(CommonModelViewset):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ["username"]

    def get_serializer_class(self):
        if self.action == "reset_password":
            return ChangePasswordSerializer
        return super().get_serializer_class()

    @action(
        permission_classes=[IsAuthenticated],
        methods=["post"],
        url_path="reset-password",
        detail=True,
    )
    def reset_password(self, request, pk=None):
        reset_password_serializer = ChangePasswordSerializer(
            request.user, data=request.data, context={"request": request}
        )

        reset_password_serializer.is_valid(raise_exception=True)
        reset_password_serializer.save()
        return Response(
            {"success": ["Password reset successfully"]}, status=status.HTTP_200_OK
        )

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()

        return instance


class CustomerViewSet(CommonModelViewset):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    search_fields = ["username"]
    permission_classes_by_action = {
        "list": [AllowAny],
        "retrieve": [IsAuthenticated | CustomerPermssion],
        "create": [IsAdminUser],
        "update": [IsAuthenticated],
    }

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except:
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetCustomerSerializer
        return super().get_serializer_class()


class SupplierViewSet(CommonModelViewset):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    search_fields = ["username"]

    # permission_classes = [SupplierPermission]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetSupplierSerializer
        return super().get_serializer_class()

    def create(self, request):
        request.data["supplier_code"] = f"SC-{Supplier.objects.count()}"
        serializers = SupplierSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(created_by=request.user)
        return Response(serializers.data, status=status.HTTP_201_CREATED)


class BillerViewSet(CommonModelViewset):
    queryset = Biller.objects.all()
    serializer_class = BillerSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetBillerSerializer
        return super().get_serializer_class()

    def create(self, request):
        request.data["biller_code"] = f"BC-{Biller.objects.count()}"
        serializers = BillerSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(created_by=request.user)
        return Response(serializers.data, status=status.HTTP_201_CREATED)


def generate_otp():
    secret_key = pyotp.random_base32()
    totp = pyotp.TOTP(secret_key)
    return totp.now()


class ForgotPasswordView(ModelViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        # using email serializer to validate the user password
        email_serializer = EmailSerializer(data=request.data)
        email_serializer.is_valid(raise_exception=True)
        email = email_serializer.validated_data["email"]

        # getting the user after validating email
        user = get_object_or_404(User, email=email)
        otp = generate_otp()

        user.otp = otp
        user.save()

        reset_password_url = (
            f"http://127.0.0.1:8000/api/forgot-password/{user.id}/change-password/"
        )

        send_otp_email(user.email, reset_password_url, otp)

        return Response(
            {"success": "Email has been sent successfully", "data": {"id": user.id}},
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=["POST"],
        detail=True,
        url_path="change-password",
        permission_classes=[AllowAny],
    )
    def change_password(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        # validating otp, password and getting the new password from the user
        forgot_password_serializer = ForgotPasswordSerializer(
            data=request.data, context={"user": user}
        )
        forgot_password_serializer.is_valid(raise_exception=True)
        password = forgot_password_serializer.validated_data["password"]

        # updating the user password
        user.set_password(password)
        user.save()

        # return success response after updating the password
        return Response(
            {"success": "Password reset successful"}, status=status.HTTP_202_ACCEPTED
        )
