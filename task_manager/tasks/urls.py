from django.urls import path
from .views import TaskViewSet, TaskDetailsViewSet

urlpatterns = [
    path('tasks/', TaskViewSet.as_view({
        "post": "create",
        "get": "list"
    }),name="task_list"),

    path('tasks/<int:pk>', TaskDetailsViewSet.as_view({
        "get": "retrieve",
        "patch": "partial_update",
        "put": "update",
        "delete": "destroy"
    }),name="task_details"),
]