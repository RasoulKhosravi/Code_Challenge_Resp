from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrAdmin
from django_filters.rest_framework import DjangoFilterBackend

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated,]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'created_at']
    http_method_names = ["post", "get"]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

class TaskDetailsViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'created_at']
    http_method_names = ["put", "get", "patch", "delete"]
