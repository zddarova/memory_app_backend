from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, Memory
from .serializers import MemorySerializer
from uuid import UUID


class MemoryCreateAPIView(APIView):
    def get(self, request):
        uuid_str = request.query_params.get('user_id')
        user_id_from_request = UUID(uuid_str)

        # Retrieve the memories for the specified user
        memories = Memory.objects.filter(user__uuid=user_id_from_request)

        # Serialize the memories
        serializer = MemorySerializer(memories, many=True)

        # Prepare the response data
        response_data = {
            'status': 'success',
            'data': {
                uuid_str: serializer.data
            }
        }

        return Response(response_data)


    def post(self, request):
        user_id = UUID(request.data.get('user_id'))
        memory_data = request.data.get('memory')

        try:
            User.objects.get(uuid=user_id)
        except User.DoesNotExist:
            User.objects.create(uuid=user_id)


        # Convert UUID to string
        user_id_str = str(user_id)

        # Assign converted UUID to user field
        memory_data['user_id'] = user_id_str

        memory_serializer = MemorySerializer(data=memory_data)

        if memory_serializer.is_valid():
            memory = memory_serializer.create(memory_data)

            response_data = {
                'status': 'success',
                'data': {
                    'userId': user_id,
                    'memory': {
                        'muid': str(memory.uuid),
                        'title': memory.title,
                        'description': memory.description,
                        'date': memory.date.isoformat()
                    }
                }
            }

            return Response(response_data, status=201)
        else:
            return Response(memory_serializer.errors, status=400)
        

    def put(self, request):
        user_id = request.data.get('userId')
        memory_data = request.data.get('memory')
        muid = memory_data['muid']

        try:
            memory = Memory.objects.get(uuid=muid)
        except Memory.DoesNotExist:
            return Response({'error': 'Memory not found.'}, status=404)

        serializer = MemorySerializer(memory, data=memory_data)
        if serializer.is_valid():
            memory = serializer.save()

            response_data = {
                'status': 'success',
                'data': {
                    'userId': user_id,
                    'memory': {
                        'muid': muid,
                        'title': memory.title,
                        'description': memory.description,
                        'date': memory.date.isoformat()
                    }
                }
            }

            return Response(response_data)
        else:
            return Response(serializer.errors, status=400)


    def delete(self, request):
        user_id = request.data.get('userId')
        memory_uuid = request.data.get('muid')

        try:
            memory = Memory.objects.get(uuid=memory_uuid)
        except Memory.DoesNotExist:
            return Response({'error': 'Memory not found.'}, status=404)

        memory.delete()

        response_data = {
            'status': 'success',
            'data': {
                'userId': user_id,
                'memoryUUID': memory_uuid
            }
        }

        return Response(response_data)
        

