from uuid import UUID
from rest_framework import serializers
from .models import User, Memory


class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ['title', 'description', 'date']

    def create(self, data):
        user_id = UUID(data.pop('user_id'))
        user = User.objects.get(uuid=user_id)
        memory = Memory.objects.create(user=user, **data)
        return memory
