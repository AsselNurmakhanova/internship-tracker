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

	def test_user_can_edit_their_internship(self):
		internship = Internship.objects.create(
			user=self.user,
			company='Northstar Labs',
			role='Design Intern',
		)
		prefix = f'internship-{internship.pk}'

		response = self.client.post(reverse('edit_internship', args=[internship.pk]), {
			f'{prefix}-company': 'Updated Labs',
			f'{prefix}-role': 'Product Design Intern',
			f'{prefix}-status': 'applied',
			f'{prefix}-date_applied': '2026-10-30',
			f'{prefix}-job_url': '',
			f'{prefix}-notes': 'Follow up next week',
		}, HTTP_HX_REQUEST='true')

		self.assertEqual(response.status_code, 200)
		internship.refresh_from_db()
		self.assertEqual(internship.company, 'Updated Labs')
		self.assertEqual(internship.status, 'applied')
		self.assertContains(response, 'Updated Labs')

	def test_user_cannot_edit_another_users_internship(self):
		other_user = User.objects.create_user(username='another-student', password='safe-test-password')
		internship = Internship.objects.create(
			user=other_user,
			company='Private Labs',
			role='Intern',
		)

		response = self.client.get(reverse('edit_internship', args=[internship.pk]))

		self.assertEqual(response.status_code, 404)

	def test_user_can_delete_their_internship_with_htmx(self):
		internship = Internship.objects.create(
			user=self.user,
			company='Northstar Labs',
			role='Design Intern',
		)

		response = self.client.post(
			reverse('delete_internship', args=[internship.pk]),
			{'q': ''},
			HTTP_HX_REQUEST='true',
		)

		self.assertEqual(response.status_code, 200)
		self.assertFalse(Internship.objects.filter(pk=internship.pk).exists())
		self.assertContains(response, 'id="internship-count"')
		self.assertContains(response, 'Your tracker is ready')

	def test_user_cannot_delete_another_users_internship(self):
		other_user = User.objects.create_user(username='another-student', password='safe-test-password')
		internship = Internship.objects.create(
			user=other_user,
			company='Private Labs',
			role='Intern',
		)

		response = self.client.post(
			reverse('delete_internship', args=[internship.pk]),
			HTTP_HX_REQUEST='true',
		)

		self.assertEqual(response.status_code, 404)
		self.assertTrue(Internship.objects.filter(pk=internship.pk).exists())

	def test_active_search_returns_only_matching_users_internships(self):
		Internship.objects.create(user=self.user, company='Northstar Labs', role='Designer')
		other_user = User.objects.create_user(username='another-student', password='safe-test-password')
		Internship.objects.create(user=other_user, company='Northstar Labs', role='Engineer')
		Internship.objects.create(user=self.user, company='Southwind', role='Engineer')

		response = self.client.get(
			reverse('main'),
			{'q': 'Northstar'},
			HTTP_HX_REQUEST='true',
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Designer')
		self.assertNotContains(response, 'Engineer')
		self.assertNotContains(response, 'Southwind')

	def test_user_can_edit_their_profile(self):
		response = self.client.post(
			reverse('edit_profile'),
			{'first_name': 'Taylor', 'last_name': 'Student'},
			HTTP_HX_REQUEST='true',
		)

		self.assertEqual(response.status_code, 200)
		self.user.refresh_from_db()
		self.assertEqual(self.user.get_full_name(), 'Taylor Student')
		self.assertContains(response, 'Taylor Student')
