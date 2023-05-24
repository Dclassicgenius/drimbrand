from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from store.models import Product, Category
from django.contrib.auth import get_user_model

from store.models import Product

class AccountModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='john@example.com',
            password='testpass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'john@example.com')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.username, 'johndoe')

    def test_full_name(self):
        self.assertEqual(self.user.full_name(), 'John Doe')

    def test_str_representation(self):
        self.assertEqual(str(self.user), self.user.email)

    def test_has_perm(self):
        self.assertFalse(self.user.has_perm(None))

    def test_has_module_perms(self):
        self.assertTrue(self.user.has_module_perms(None))

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='john@example.com',
            password='testpass123'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            address_line_1='123 Main St',
            address_line_2='Apt 4B',
            city='New York',
            state='NY',
            country='USA'
        )

    def test_str_representation(self):
        self.assertEqual(str(self.user_profile), self.user.first_name)

    def test_full_address(self):
        self.assertEqual(self.user_profile.full_address(), '123 Main St Apt 4B')


class RegistrationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '1234567890',
            'email': 'john@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '1234567890',
            'email': 'john@example.com',
            'password': 'testpass123',
            'confirm_password': 'wrongpass123',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

class UserFormTest(TestCase):
    def test_valid_form(self):
        user = Account.objects.create(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='john@example.com',
            password='testpass123'
        )
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '1234567890',
        }
        form = UserForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())

class UserProfileFormTest(TestCase):
    def test_valid_form(self):
        user = Account.objects.create(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='john@example.com',
            password='testpass123'
        )
        image = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        form_data = {
            'address_line_1': '123 Main St',
            'address_line_2': 'Apt 4B',
            'city': 'New York',
            'state': 'NY',
            'country': 'USA',
            'profile_picture': image,
        }
        form = UserProfileForm(data=form_data, files={'profile_picture': image}, instance=user)
        self.assertTrue(form.is_valid())
