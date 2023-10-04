from django.contrib.auth import get_user_model
from django.test import TestCase

from agency.models import Topic, Newspaper


class ModelTest(TestCase):
    def setUp(self) -> None:
        self.redactor = get_user_model().objects.create_user(
            username="test",
            password="123",
            first_name="Test",
            last_name="Test",
        )
        self.topic = Topic.objects.create(name="Test")
        self.newspaper = Newspaper.objects.create(
            title="Test",
            content="Test",
            topic=self.topic,
        )
        self.newspaper.publishers.add(self.redactor)

    def test_redactor_str(self):
        self.assertEqual(str(self.redactor), self.redactor.username)

    def test_topic_str(self):
        self.assertEqual(str(self.topic), self.topic.name)

    def test_newspaper_str(self):
        self.assertEqual(str(self.newspaper), self.newspaper.title)
