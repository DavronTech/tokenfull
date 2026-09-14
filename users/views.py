from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serilazers import SignUpSerilazers,LoginSerilazers,ProfileSerializer



class SigUpView(APIView):
    def post(self, request):
        serilazer = SignUpSerilazers(data=request.data)
        serilazer.is_valid(raise_exception=True)
        serilazer.validated_data.pop('confirm_password')
        user = User.objects.create_user(**serilazer.validated_data)


        return Response({
            'msg': 'signup',
            'user': SignUpSerilazers(user).data
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerilazers(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return Response(
                {'error': 'Username yoki password noto‘g‘ri'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key
        })

class ProfileView(APIView):

    def get(self, request):
        user = request.user

        serializer = ProfileSerializer(user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        request.auth.delete()

        return Response(
            {
                'msg': 'Logout successful'
            },
            status=status.HTTP_200_OK
        )