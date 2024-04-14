from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from accounts.serializers import (
    UserAccountSerializer,
    UserAccountVerificationSerializer,
    AccountDeletionSerializer,
    UpdateUserAccountEmailSerializer,
    UpdateUserAccountNameSerializer,
    RegenerateVerificationCodeSerializer,
)
from accounts.models import User


class AccountRegistrationView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserAccountSerializer
    queryset = User.objects.all()


class AccountVerificationView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserAccountVerificationSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)


class RegenerateVerificationCode(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegenerateVerificationCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegenerateVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class AccountDetailsView(APIView):
    serializer_class = UserAccountSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)


# contacts
class UserContactsListView(APIView):
    serializer_class = UserAccountSerializer

    def get_queryset(self):
        queryset = User.objects.filter(is_active=True).exclude(
            id=self.request.user.id
        )
        return queryset

    def get(self, request, *args, **kwargs):
        serializer = UserAccountSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class UpdateUserAccountEmailView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserAccountEmailSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            instance=request.user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        data = UserAccountSerializer(obj).data
        return Response(data)


class UpdateUserAccountNameView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserAccountNameSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            instance=request.user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        data = UserAccountSerializer(obj).data
        return Response(data)


class AccountDeleteView(APIView):
    serializer_class = AccountDeletionSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
