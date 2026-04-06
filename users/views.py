from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from users.models import User
from users.serializers import UserCreateSerializer, UserRetrieveSerializer


class UserCreateView(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer

    @extend_schema(summary='Create new user')
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Get user')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)