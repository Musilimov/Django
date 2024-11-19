from django.test import TestCase
from notifications.tasks import send_notification  # Импорт задачи Celery

class CeleryTaskTest(TestCase):

    def test_send_notification(self):
        result = send_notification.apply(args=["test@example.com", "Notification message"])
        self.assertTrue(result.successful())
