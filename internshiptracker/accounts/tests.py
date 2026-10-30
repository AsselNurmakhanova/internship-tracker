from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Internship


class InternshipDashboardTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='student', password='safe-test-password')
		self.client.force_login(self.user)

	def test_dashboard_requires_login(self):
		self.client.logout()
		response = self.client.get(reverse('main'))

		self.assertRedirects(response, f"{reverse('login')}?next={reverse('main')}")

	def test_user_can_add_internship(self):
		response = self.client.post(reverse('main'), {
			'company': 'Northstar Labs',
			'role': 'Product Design Intern',
			'status': 'applied',
			'date_applied': '2026-10-30',
			'job_url': 'https://example.com/jobs/123',
			'notes': 'Follow up next week',
		})

		self.assertRedirects(response, reverse('main'))
		internship = Internship.objects.get(user=self.user)
		self.assertEqual(internship.company, 'Northstar Labs')
		self.assertEqual(internship.status, 'applied')

	def test_invalid_submission_reopens_form_with_errors(self):
		response = self.client.post(reverse('main'), {
			'company': '',
			'role': 'Product Design Intern',
			'status': 'wishlist',
		})

		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context['show_add_modal'])
		self.assertIn('company', response.context['form'].errors)
		self.assertEqual(Internship.objects.count(), 0)

	def test_logout_clears_session_and_returns_to_login(self):
		response = self.client.post(reverse('logout'))

		self.assertRedirects(response, reverse('login'))
		self.assertNotIn('_auth_user_id', self.client.session)
