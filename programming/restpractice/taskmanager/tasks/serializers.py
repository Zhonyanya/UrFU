from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Project, Task


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        """Метакласс."""

        model = User
        fields = ('id', 'username', 'email')


class ProjectSerializer(serializers.ModelSerializer):
    """Сериализатор проекта."""

    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        """Метакласс."""

        model = Project
        fields = ('id', 'name', 'creator', 'members')
        read_only_fields = ('id', 'creator')

    def create(self, validated_data):
        """Создание."""
        request = self.context.get('request')

        if not request.user.is_authenticated:
            raise ValidationError()

        validated_data.pop('creator', None)

        project = Project.objects.create(
            creator=request.user,
            **validated_data
        )
        project.members.add(request.user)
        return project


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор задачи."""

    class Meta:
        """Метакласс."""

        model = Task
        fields = ('id', 'title', 'description', 'priority', 'status',
                  'deadline', 'project', 'author', 'executor')
        read_only_fields = ('id', 'author')

    def validate(self, data):
        """Валидация."""
        project = data.get('project')
        executor = data.get('executor')
        if executor and executor not in project.members.all():
            raise ValidationError()
        return data

    def create(self, validated_data):
        """Создаёт задачу."""
        request = self.context.get('request')

        if not request.user.is_authenticated:
            raise ValidationError()

        validated_data.pop('author', None)

        task = Task.objects.create(
            author=request.user,
            **validated_data
        )
        return task
