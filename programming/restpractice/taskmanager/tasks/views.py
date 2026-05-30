from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, Task
from rest_framework import viewsets, status
from .serializers import ProjectSerializer, TaskSerializer, UserSerializer
from django.db.models import Q
# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    """Вьюсет проекта."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """Возвращает только те проекты, которые доступны пользователю."""
        user = self.request.user
        return Project.objects.filter(members=user)

    def perform_create(self, serializer):
        """Добавляет создателя в участники."""
        project = serializer.save(creator=self.request.user)
        project.members.add(self.request.user)
    
    @action(detail=True, methods=['post'], url_path='add-member')
    def add_member(self, request, pk=None):
        """Добавление участника в проект (только для владельца)."""
        project = self.get_object()
        
        # Проверка: только владелец может добавлять участников
        if project.creator != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if user in project.members.all():
            return Response(status=status.HTTP_200_OK)
        
        project.members.add(user)
        
        return Response({
            'success': True,
            'message': f'Пользователь {user.username} добавлен в проект {project.name}',
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='remove-member')
    def remove_member(self, request, pk=None):
        """Удаление участника из проекта (только для владельца)."""
        project = self.get_object()
        
        if project.creator != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if user == project.creator:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if user not in project.members.all():
            return Response(status=status.HTTP_200_OK)
        
        project.members.remove(user)
        
        return Response({
            'success': True,
            'message': f'Пользователь {user.username} удален из проекта {project.name}',
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)


class TaskViewSet(viewsets.ModelViewSet):
    """Вьюсет задачи."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        """Возвращает только те задачи, которые доступны пользователю."""
        user = self.request.user

        return Task.objects.filter(
            Q(project__creator=user) |
            Q(author=user) |
            Q(executor=user)
        ).distinct()
    
    def perform_create(self, serializer):
        """Сохраняет и так добавляет автора задачи автоматически."""
        serializer.save()

    @action(detail=True, methods=['post'], url_path='edit-title')
    def edit_title(self, request, pk=None):
        """
        Редактирование заголовка задачи.
        """
        task = self.get_object()

        if task.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        new_title = request.data.get('title')
        if not new_title:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        old_title = task.title
        task.title = new_title
        task.save()

        return Response({
            'task_id': task.id,
            'message': 'Заголовок задачи обновлён',
            'old_title': old_title,
            'new_title': task.title
        }
        )
    
    @action(detail=True, methods=['post'], url_path='edit-description')
    def edit_description(self, request, pk=None):
        """Редактирование описания."""
        
        task = self.get_object()

        if task.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        new_description = request.data.get('description')
        if not new_description:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        old_description = task.description
        task.description = new_description
        task.save()

        return Response({
            'task_id': task.id,
            'message': 'Описание задачи обновлено',
            'old_description': old_description,
            'new_description': task.title
        }
        )
    @action(detail=True, methods=['post'], url_path='edit-priority')
    def edit_priority(self, request, pk=None):
        """Редактирование приоритета."""

        task = self.get_object()



class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
