from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from agency.models import Topic, Newspaper

HOME_URL = reverse('agency:index')

CREATE_URL = reverse('agency:newspaper-create')


class SetUpMixin:
	def setUp(self) -> None:
		self.redactor = get_user_model().objects.create_user(
			username='test',
			password='123',
			first_name='Test',
			last_name='Test',
		)
		self.topic = Topic.objects.create(name='Test')
		self.newspaper = Newspaper.objects.create(
			title='Test',
			content='Test',
			topic=self.topic,
		)
		self.newspaper.publishers.add(self.redactor)


class PublicHomeViewTest(SetUpMixin, TestCase):
	def test_retrive_newspapers(self):
		newspaper_list = Newspaper.objects.all()
		response = self.client.get(HOME_URL)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'agency/index.html')
		self.assertEqual(
			list(response.context['newspaper_list']),
			list(newspaper_list)
		)


class PublicNewspaperViewTest(SetUpMixin, TestCase):

	def test_retrive_newspaper(self):
		response = self.client.get(reverse('agency:newspaper-detail', kwargs={'pk': self.newspaper.pk}))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.newspaper.title)
		self.assertContains(response, self.newspaper.content)
		self.assertContains(response, self.redactor.username)


class PublicCreateViewTest(SetUpMixin, TestCase):
	def test_login_required(self):
		response = self.client.get(CREATE_URL)
		self.assertNotEqual(response.status_code, 200)


class PrivateCreateViewTest(SetUpMixin, TestCase):
	def test_redactor_can_create_newspaper(self):
		self.client.force_login(self.redactor)
		response = self.client.post(CREATE_URL, {
			'title': 'Test',
			'content': 'Test',
			'topic': self.topic.pk,
			'publishers': self.redactor.pk
		})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Newspaper.objects.last().title, 'Test')
