from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, Memory
from .serializers import MemorySerializer
from uuid import UUID

user_id_key = 'user_id'
status_key = 'status'
status_value = 'success'
data_key = 'data'
memory_key = 'memory'
muid_key = 'muid'
title_key = 'title'
description_key = 'description'
date_key = 'date'

class MemoryCreateAPIView(APIView):
    def get(self, request):
        uuid_str = request.query_params.get(user_id_key)
        user_id_from_request = UUID(uuid_str)

        # Retrieve the memories for the specified user
        memories = Memory.objects.filter(user__uuid=user_id_from_request)

        # Serialize the memories
        serializer = MemorySerializer(memories, many=True)

        # Prepare the response data
        response_data = {
            status_key: status_value,
            data_key: {
                uuid_str: serializer.data
            }
        }

        return Response(response_data)


    def post(self, request):
        user_id = UUID(request.data.get(user_id_key))
        memory_data = request.data.get(memory_key)

        try:
            User.objects.get(uuid=user_id)
        except User.DoesNotExist:
            User.objects.create(uuid=user_id)


        # Convert UUID to string
        user_id_str = str(user_id)

        # Assign converted UUID to user field
        memory_data[user_id_key] = user_id_str

        memory_serializer = MemorySerializer(data=memory_data)

        if memory_serializer.is_valid():
            memory = memory_serializer.create(memory_data)

            response_data = {
                status_key: status_value,
                data_key: {
                    user_id_key: user_id,
                    memory_key: {
                        muid_key: str(memory.uuid),
                        title_key: memory.title,
                        description_key: memory.description,
                        date_key: memory.date.isoformat()
                    }
                }
            }

            return Response(response_data, status=201)
        else:
            return Response(memory_serializer.errors, status=400)
        

    def put(self, request):
        user_id = request.data.get(user_id_key)
        memory_data = request.data.get(memory_key)
        muid = memory_data[muid_key]

        try:
            memory = Memory.objects.get(uuid=muid, user__uuid = user_id)
        except Memory.DoesNotExist:
            return Response({'error': 'Memory not found.'}, status=404)

        serializer = MemorySerializer(memory, data=memory_data)
        if serializer.is_valid():
            memory = serializer.save()

            response_data = {
                status_key: status_value,
                data_key: {
                    user_id_key: user_id,
                    memory_key: {
                        muid_key: muid,
                        title_key: memory.title,
                        description_key: memory.description,
                        date_key: memory.date.isoformat()
                    }
                }
            }

            return Response(response_data)
        else:
            return Response(serializer.errors, status=400)


    def delete(self, request):
        user_id = request.data.get(user_id_key)
        memory_uuid = request.data.get(muid_key)

        try:
            memory = Memory.objects.get(uuid=memory_uuid)
        except Memory.DoesNotExist:
            return Response({'error': 'Memory not found.'}, status=404)

        memory.delete()

        response_data = {
            status_key: status_value,
            data_key: {
                user_id_key: user_id,
                muid_key: memory_uuid
            }
        }

        return Response(response_data)
        

