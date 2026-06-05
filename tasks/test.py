from django.test import TestCase
from .models import Task

class TaskTest(TestCase):

    def test_task_creation(self):
        task = Task.objects.create(
            title="Deploy Application"
        )

        self.assertEqual(
            task.title,
            "Deploy Application"
        )