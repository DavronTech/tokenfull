from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serilazers import SignUpSerilazers,LoginSerilazers,ProfileSerializer,LogoutSerializer, PasswordChangeSerializer



class SigUpView(APIView):

    def post(self, request):
        serializer = SignUpSerilazers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                'msg': 'Signup successful',
                'user': SignUpSerilazers(user).data
            },status=status.HTTP_201_CREATED
        )


class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerilazers(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            'msg': 'Login successful',
            'token': serializer.validated_data['token']
        })


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request):

        serializer = ProfileSerializer(request.user,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=status.HTTP_200_OK)

    def patch(self, request):

        serializer = ProfileSerializer(request.user,data=request.data,partial=True)
        serializer.is_valid( raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=status.HTTP_200_OK)

class PasswordChangeView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data,context={'request': request })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'msg': 'Password changed successfully'
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(data={},context={ 'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'msg': 'Logout successful'
            },
            status=status.HTTP_200_OK
        )