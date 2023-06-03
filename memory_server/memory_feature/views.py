from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Memory
from .serializers import MemorySerializer

@api_view(['GET'])
def memory_list_create(request):
    if request.method == 'GET':
        memories = Memory.objects.all()
        serializer = MemorySerializer(memories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MemorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['POST', 'PUT', 'DELETE'])
def memory_retrieve_update_destroy(request, pk):
    try:
        memory = Memory.objects.get(pk=pk)
    except Memory.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = MemorySerializer(memory)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MemorySerializer(memory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        memory.delete()
        return Response(status=204)
