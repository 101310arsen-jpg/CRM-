from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')

        if status is not None:
            valid_statuses = ['todo', 'in_progress', 'done']
            if status not in valid_statuses:
                raise ValidationError({
                    'status': 'Недопустимый статус'
                })
            queryset = queryset.filter(status=status)

        if priority is not None:
            valid_priorities = ['low', 'medium', 'high']
            if priority not in valid_priorities:
                raise ValidationError({
                    'priority': 'Недопустимый приоритет'
                })
            queryset = queryset.filter(priority=priority)

        return queryset


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer