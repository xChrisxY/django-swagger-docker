from .serializer import TaskSerializer
from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Task
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='post',
    request_body=TaskSerializer,  # Qué datos espera (input)
    responses={201: TaskSerializer, 400: "Bad Request"}  # Qué responde
)
# Create your views here.
@api_view(['POST'])
#@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_task(request):
    
    # añadimos el usuario autenticado como propietario
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):
    
    try:
        task = Task.objects.get(pk=pk)
    except:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response({"message": "success", "task": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        print("para hacer uptading")
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "success", "task": serializer.data}, status=status.HTTP_200_OK)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            task.delete()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Can't delete task", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_tasks_by_status(request):

    completed = request.query_params.get('completed')

    if completed is None:
        return Response({"error": "Missing 'completed' query parameter (expected 'true' or 'false')"}, status=status.HTTP_400_BAD_REQUEST)

    try:

        completed = completed.lower() == 'true'
        tasks = Task.objects.filter(owner=request.user, completed=completed)
        serializer = TaskSerializer(tasks, many=True)
        return Response({"message": "success", "tasks": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_task_completed(request, pk):

    try:
        task = Task.objects.get(pk=pk, owner=request.user)
    except Task.DoesNotExist:
        return Response({"error": "Task not found or you don't have permission to modify it"}, status=status.HTTP_404_NOT_FOUND)
    
    task.completed = True   
    task.save()
    serializer = TaskSerializer(task)
    return Response({"message": "Task marked as completed", "task": serializer.data}, status=status.HTTP_200_OK)
