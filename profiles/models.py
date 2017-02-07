from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
	user = models.OneToOneField(User, blank=True, null=True)
	name = models.CharField(max_length=255)
	description = models.TextField()
	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.name