from django.db import models
from django.contrib.auth.models import User


class Internship(models.Model):
	STATUS_CHOICES = [
		('wishlist', 'Wishlist'),
		('applied', 'Applied'),
		('assessment', 'Assessment'),
		('interview', 'Interview'),
		('offer', 'Offer'),
		('rejected', 'Rejected'),
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='internships')
	company = models.CharField(max_length=120)
	role = models.CharField(max_length=160)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='wishlist')
	date_applied = models.DateField(blank=True, null=True)
	job_url = models.URLField(blank=True)
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.role} at {self.company}'
