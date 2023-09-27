from django.contrib.auth.models import AbstractUser
from django.db import models


class Redactor(AbstractUser):
	years_of_experience = models.PositiveIntegerField()
	
	class Meta:
		verbose_name = 'redactor'
		verbose_name_plural = 'redactors'


class Topic(models.Model):
	name = models.CharField(max_length=255)
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = 'topic'
		verbose_name_plural = 'topics'
		ordering = ['name']
		
		
class Newspaper(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField()
	published_date = models.DateTimeField(auto_now_add=True)
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	publishers = models.ManyToManyField(Redactor)
	
	def __str__(self):
		return self.title
	
	class Meta:
		verbose_name = 'newspaper'
		verbose_name_plural = 'newspapers'
		ordering = ['name']