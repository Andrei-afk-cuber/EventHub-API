from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import UserCreateSerializer, UserRetrieveSerializer


class UserCreateView(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer

class UserRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = [IsAuthenticated]