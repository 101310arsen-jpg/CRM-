from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task


class TaskAPITests(APITestCase):

    def setUp(self):
        self.task = Task.objects.create(
            title="Первая задача",
            description="Проверка REST API",
            status="todo",
            priority="high"
        )

    def test_get_tasks(self):
        response = self.client.get(reverse("task-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_task(self):
        data = {
            "title": "Новая задача",
            "description": "Создание через API",
            "status": "todo",
            "priority": "medium"
        }

        response = self.client.post(
            reverse("task-list"),
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_get_single_task(self):
        response = self.client.get(
            reverse("task-detail", args=[self.task.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task(self):
        response = self.client.patch(
            reverse("task-detail", args=[self.task.id]),
            {"status": "done"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "done")

    def test_delete_task(self):
        response = self.client.delete(
            reverse("task-detail", args=[self.task.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_invalid_title(self):
        response = self.client.post(
            reverse("task-list"),
            {"title": "   "},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_task_not_found(self):
        response = self.client.get(
            reverse("task-detail", args=[99999])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_tasks(self):
        response = self.client.get(
            reverse("task-list"),
            {"status": "todo"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)