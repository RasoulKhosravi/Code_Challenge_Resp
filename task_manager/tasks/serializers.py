from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'created_at', 'updated_at', 'user']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def create(self, validated_data):
        validated_data.pop('user', None)
        user = self.context['request'].user
        task = Task.objects.create(user=user, **validated_data)
        return task