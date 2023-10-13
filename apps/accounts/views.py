from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
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
    ChangePasswordSerializer,
    EmailSerializer,
    ForgotPasswordSerializer,
)
from utils.pagination import MyPagination
from utils.emails import send_otp_email
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
# from utils.permissions import CustomerPermssion, SupplierPermssion
from apps.accounts.utils import generate_otp
from apps.accounts.models import OTP
from decouple import config


class CommonModelViewset(ModelViewSet):
    pagination_class = MyPagination


class UserViewSet(CommonModelViewset):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ["username"]
    permission_classes_by_action = {
        "list": [AllowAny],
        "retrieve": [IsAuthenticated],
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
        if self.action == "reset_password":
            return ChangePasswordSerializer
        return super().get_serializer_class()

    @action(methods=["post"], url_path="reset-password", detail=True)
    def reset_password(self, request, pk=None):
        reset_password_serializer = ChangePasswordSerializer(
            request.user, data=request.data, context={"request": request}
        )

        reset_password_serializer.is_valid(raise_exception=True)
        reset_password_serializer.save()
        return Response(
            {"success": ["Password reset successfully"]}, status=status.HTTP_200_OK
        )

    @action(methods=["post"], url_path="forgot-password", detail=False)
    def forgot_password(self, request):
        email_serializer = EmailSerializer(data=request.data)
        email_serializer.is_valid(raise_exception=True)
        email = email_serializer.validated_data["email"]

        user = get_object_or_404(User, email=email)
        generated_otp = generate_otp()

        try:
            user_otp = OTP.objects.get(user=user)
            user_otp.otp = generated_otp
            user_otp.save()
        except OTP.DoesNotExist:
            user_otp = OTP.objects.create(user=user, otp=generated_otp)
        send_otp_email(user.email, generated_otp)

        return Response(
            {
                "success": "Email has been sent successfully",
            },
            status=status.HTTP_201_CREATED,
        )

    @action(methods=["post"], detail=False, url_path="change-password")
    def change_password(self, request):
        get_otp = request.data.get("otp")
        #get 1st matched user otp based on filter. 
        user_otp = OTP.objects.filter(otp=get_otp).first()
        if user_otp is None:
            raise ValidationError({"otp": "Enter valid OTP."})
        user = user_otp.user

        forgot_password_serializer = ForgotPasswordSerializer(data=request.data)
        forgot_password_serializer.is_valid(raise_exception=True)
        password = forgot_password_serializer.validated_data["password"]

        user.set_password(password)
        user.save()

        return Response(
            {"success": "Password reset successful"}, status=status.HTTP_202_ACCEPTED
        )


class CustomerViewSet(CommonModelViewset):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    search_fields = ["username"]
    permission_classes_by_action = {
        "list": [AllowAny],
        "retrieve": [IsAuthenticated ],
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

    def create(self, request):
        # Extract user data from the request
        user_data = request.data.pop("user", None)
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(role="Customer")

        customer_serializer = CustomerSerializer(data={**request.data})
        if customer_serializer.is_valid():
            customer_serializer.save(
                user=user,
                created_by=request.user,
            )
            return Response(customer_serializer.data, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response(
                customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetCustomerSerializer
        return super().get_serializer_class()


class SupplierViewSet(CommonModelViewset):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    search_fields = ["username"]
    permission_classes_by_action = {
        "list": [AllowAny],
        "retrieve": [IsAuthenticated],
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

    def create(self, request):
        # Extract user data from the request
        user_data = request.data.pop("user", None)
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(role="Supplier")

        supplier_serializer = SupplierSerializer(data={**request.data})

        # SUPPLIER_PREFIX = config("SUPPLIER_PREFIX", default="")
        if supplier_serializer.is_valid():
            supplier_serializer.save(
                user=user,
                created_by=request.user,
                # supplier_code=f"{SUPPLIER_PREFIX}{Supplier.objects.count()}",
            )
            return Response(supplier_serializer.data, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response(
                supplier_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetSupplierSerializer
        return super().get_serializer_class()


class BillerViewSet(CommonModelViewset):
    queryset = Biller.objects.all()
    serializer_class = BillerSerializer
    permission_classes_by_action = {
        "list": [AllowAny],
        "retrieve": [IsAuthenticated],
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

    def create(self, request):
        # Extract user data from the request
        user_data = request.data.pop("user", None)
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(role="Biller")

        biller_serializer = BillerSerializer(data={**request.data})
        BILLER_PREFIX = config("BILLER_PREFIX", default="")

        if biller_serializer.is_valid():
            biller_serializer.save(
                user=user,
                created_by=request.user,
                biller_code=f"{BILLER_PREFIX}{Biller.objects.count()}",
            )
            return Response(biller_serializer.data, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response(
                biller_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetBillerSerializer
        return super().get_serializer_class()
