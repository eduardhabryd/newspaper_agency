from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models


class Redactor(AbstractUser):
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='redactors', null=True)

    class Meta:
        verbose_name = 'redactor'
        verbose_name_plural = 'redactors'
        default_related_name = 'redactors'

    def __str__(self):
        return self.username


class Topic(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'topic'
        verbose_name_plural = 'topics'
        ordering = ['name']

    def __str__(self):
        return self.name

    def image_name(self):
        return self.name.lower().replace(' ', '_') + '.svg'


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='newspapers')
    publishers = models.ManyToManyField(Redactor, related_name='newspapers')
    image = models.ImageField(upload_to='newspaper_images', null=True)

    class Meta:
        verbose_name = 'newspaper'
        verbose_name_plural = 'newspapers'
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_short_content(self):
        if len(self.content) > 75:
            return self.content[:75] + '...'
        return self.content

    def get_content_list(self):
        return self.content.split('\n')

    def get_publishers(self):
        output = []
        for publisher in self.publishers.all():
            output.append(
                {
                    "name": publisher.first_name + " " + publisher.last_name,
                    "id": publisher.id
                }
            )

        return output
