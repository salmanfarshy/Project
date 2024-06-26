from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Users, Projects, Tasks, Comments
from .serializers import UserSerializer, ProjectSerializer, TasksSerializer, CommentsSerializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny

# token obtain view
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

class MyTokenRefreshView(TokenRefreshView):
    pass  # Default behavior is sufficient for token refresh

# users view
class RegisterView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            response_data['password'] = data['password']
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        email = data.get('email')
        password = data.get('password')
        if not email: return Response({'Error': 'Email is required.' })
        try:
            user = Users.objects.get(email=email)
            if user.password == password:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username,
                    }
                })
            else:
                return Response({'Error': 'Wrong Password.' })
        except Users.DoesNotExist:
            return Response({'Error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        return obj
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({
            'message': 'User deleted successfully.'
        }, status=status.HTTP_204_NO_CONTENT)

# projects view
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        projects = self.get_queryset()
        if not projects.exists():
            return Response({"Error": "Projects are not available."}, status=status.HTTP_404_NOT_FOUND)
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            project = self.get_object()
            return Response(self.get_serializer(project).data)
        except Projects.DoesNotExist:
            return Response({"Error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        try:
            project = self.get_object()
            return super().put(request, *args, **kwargs)
        except Projects.DoesNotExist:
            return Response({"Error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        try:
            # project = self.get_object()
            super().delete(request, *args, **kwargs)
            return Response({
                'message': 'Project deleted successfully.'
            }, status=status.HTTP_204_NO_CONTENT)
        except Projects.DoesNotExist:
            return Response({"Error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        
# tasks view
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Tasks.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        serializer.save(project_id=project_id)

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        # Check if the project exists
        project = Projects.objects.filter(pk=project_id).first()
        if not project:
            return Response({"Error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)
        return super().create(request, *args, **kwargs)
        
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if not obj:
            return Response({"Error": "Task not found."})
        return obj

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        self.perform_destroy(task)
        return Response({"message": "Task deleted successfully."}, status=status.HTTP_200_OK)

# comments view
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Comments.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        task = get_object_or_404(Tasks, pk=task_id)
        serializer.save(task=task, user=self.request.user)

    def create(self, request, *args, **kwargs):
        task_id = self.kwargs['task_id']
        if not Tasks.objects.filter(pk=task_id).exists():
            return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        return super().create(request, *args, **kwargs)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Comments, pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Ensure only the 'content' field is updated
        if 'content' not in request.data:
            return Response({"detail": "Content field is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance, data={'content': request.data['content']}, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response({"detail": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)