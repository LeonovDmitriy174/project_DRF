from datetime import datetime

import pytz
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from config import settings
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.last_login = datetime.now(pytz.timezone(settings.TIME_ZONE))
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        return super().get_permissions()
