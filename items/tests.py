from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.test import override_settings
from django.contrib.messages import get_messages

from .auth_forms import StudentSignUpForm
from .models import Item


class StudentSignUpFormTests(TestCase):
    def test_signup_form_saves_email(self):
        form = StudentSignUpForm(
            data={
                'username': 'student',
                'email': 'student@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            }
        )

        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertEqual(user.email, 'student@example.com')


class StudentDashboardTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='password123'
        )
        self.other_student = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='password123'
        )
        self.my_post = Item.objects.create(
            owner=self.student,
            title='Student Backpack',
            item_type='Lost',
            description='Black backpack',
            location='Auditorium',
            image='items/backpack.jpg',
            contact='1234567890'
        )
        self.claimed_item = Item.objects.create(
            owner=self.other_student,
            claimed_by=self.student,
            title='Claimed Calculator',
            item_type='Found',
            description='Scientific calculator',
            location='Lab',
            image='items/calculator.jpg',
            contact='1234567890',
            claimed=True
        )
        self.other_post = Item.objects.create(
            owner=self.other_student,
            title='Other Notes',
            item_type='Lost',
            description='Class notes',
            location='Library',
            image='items/notes.jpg',
            contact='1234567890'
        )

    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard/')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/signup/', response.url)

    def test_dashboard_shows_student_posts_and_claims(self):
        self.client.login(
            username='student',
            password='password123'
        )

        response = self.client.get('/dashboard/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Backpack')
        self.assertContains(response, 'Claimed Calculator')
        self.assertNotContains(response, 'Other Notes')
        self.assertQuerySetEqual(
            response.context['my_posts'],
            [self.my_post]
        )
        self.assertQuerySetEqual(
            response.context['claimed_items'],
            [self.claimed_item]
        )


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    DEFAULT_FROM_EMAIL='noreply@example.com',
    EMAIL_HOST_USER='noreply@example.com',
    EMAIL_HOST_PASSWORD='password'
)
class ClaimNotificationTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='password123'
        )
        self.claimer = User.objects.create_user(
            username='claimer',
            email='claimer@example.com',
            password='password123'
        )
        self.item = Item.objects.create(
            owner=self.owner,
            title='Blue Umbrella',
            item_type='Found',
            description='Found near the library',
            location='Library',
            image='items/umbrella.jpg',
            contact='1234567890'
        )

    def test_claim_sends_email_to_item_owner(self):
        self.client.login(
            username='claimer',
            password='password123'
        )

        response = self.client.get(f'/claim/{self.item.id}/')

        self.assertEqual(response.status_code, 302)

        self.item.refresh_from_db()

        self.assertTrue(self.item.claimed)
        self.assertEqual(self.item.claimed_by, self.claimer)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['owner@example.com'])
        self.assertIn('Blue Umbrella', mail.outbox[0].subject)
        self.assertIn('claimer', mail.outbox[0].body)

    def test_owner_cannot_claim_own_item(self):
        self.client.login(
            username='owner',
            password='password123'
        )

        response = self.client.get(f'/claim/{self.item.id}/')

        self.assertEqual(response.status_code, 302)

        self.item.refresh_from_db()

        self.assertFalse(self.item.claimed)
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(DEFAULT_FROM_EMAIL='')
    def test_claim_fails_when_sender_email_is_missing(self):
        self.client.login(
            username='claimer',
            password='password123'
        )

        response = self.client.get(f'/claim/{self.item.id}/')

        self.assertEqual(response.status_code, 302)

        self.item.refresh_from_db()

        self.assertFalse(self.item.claimed)
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(EMAIL_HOST_USER='', EMAIL_HOST_PASSWORD='')
    def test_claim_fails_when_smtp_login_is_missing(self):
        self.client.login(
            username='claimer',
            password='password123'
        )

        response = self.client.get(f'/claim/{self.item.id}/')

        self.assertEqual(response.status_code, 302)

        self.item.refresh_from_db()

        self.assertFalse(self.item.claimed)
        self.assertEqual(len(mail.outbox), 0)

        messages = [
            str(message)
            for message in get_messages(response.wsgi_request)
        ]

        self.assertIn(
            'Claim failed because email notifications are not configured. Add EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, and DEFAULT_FROM_EMAIL in the .env file. For Gmail, use a Google App Password, not your normal account password. Restart the server after saving .env.',
            messages
        )
