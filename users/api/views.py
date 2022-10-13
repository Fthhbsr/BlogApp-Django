from rest_framework import generics, status
from django.conf import settings
from users.api.serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from users.models import User
from django.contrib.auth import get_user_model
# User = settings.AUTH_USER_MODEL
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        if Token.objects.filter(user=user):
            token = Token.objects.get(user=user)
            data['token'] = token.key
        else:
            data['error'] = 'User does not have token . Try again ...'
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
