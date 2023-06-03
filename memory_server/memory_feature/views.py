from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import MemorySerializer
from uuid import UUID


class MemoryCreateAPIView(APIView):
    def post(self, request):
        user_id = UUID(request.data.get('user_id'))
        memory_data = request.data.get('memory')

        try:
            user = User.objects.get(uuid=user_id)
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
