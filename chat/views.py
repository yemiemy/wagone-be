from rest_framework.views import APIView
from chat.serializers import ChatSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class MessageAPIView(APIView):
    # permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatAPIView(APIView):
    # permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
