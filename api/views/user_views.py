# Essential DRF & Simple JWT imports
# Essential serializers imports
from api.serializers import (
    ProductSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserSerializerWithToken,
)
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser, User
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = settings.AUTH_USER_MODEL


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserSerializerWithToken


class UserRegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format="json"):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
            return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                "success": True,
                "status_code": status_code,
                "message": "User logged in successfully",
                "access": serializer.data["access"],
                "refresh": serializer.data["refresh"],
                "authenticatedUser": {
                    "email": serializer.data["email"],
                },
            }
            return Response(response, status=status_code)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    """
    ✅Get current login user profile.
    """
    user = request.user

    serializer = UserSerializerWithToken(user, many=False)

    data = request.data

    user.username = data["username"]
    user.email = data["email"]
    user.name = data["name"]

    if data["password"] != "":
        user.password = make_password(data["password"])

    user.save()

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    """
    ✅Update authenticate user profile.
    """
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getUsersList(request):

    """
    ✅Retrieves a list of Users.
        ♻ Method: GET
    """
    users = User.objects.all()

    superusers = User.objects.filter(is_superuser=False)
    print(superusers)
    superusers_emails = User.objects.filter(is_superuser=False).values_list("email")
    print(superusers_emails)

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateUser(request, pk):
    """

    ✅Partially updates user.
    """
    user = User.objects.get(id=pk)

    data = request.data

    user.username = data["username"]
    user.name = data["name"]
    user.email = data["email"]
    user.is_staff = data["isAdmin"]

    user.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteUser(request, pk):
    """
    🚨Deletes authenticate user account with given id.
    """
    user = User.objects.get(id=pk)
    user.delete()
    return Response("User Was Deleted Successfully!")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def deactivateUser(request, pk):
    """
    ✅Deactivate User account instead of delete.
    """
    try:
        user = User.objects.get(id=pk)
        user.is_active = False
        user.save()

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    except User.DoesNotExist:
        content = {
            "detail": "Something bad happened :( User matching query does not exist with this ID."
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    finally:
        content = {"detail": "User Deactivated Successfully"}
        return Response(content, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    """
    ✅Retrieves a specific User.
    """
    try:
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    except User.DoesNotExist:
        content = {
            "detail": "User matching query doesn't exist with this ID. Please try again with deferred user Id."
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
