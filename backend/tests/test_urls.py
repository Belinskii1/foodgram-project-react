from django.test import TestCase, Client


class PagesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_admin_login_exists(self):
        """Проверка доступности адреса /admin/"""
        response = self.guest_client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)

    def test_api_exists(self):
        """Проверка доступности адреса /admin/api/"""
        response = self.guest_client.get('/api/')
        self.assertEqual(response.status_code, 200)

    def test_api_users_exists(self):
        """Проверка доступности адреса /admin/api/users/ без логина"""
        response = self.guest_client.get('/api/users/')
        self.assertEqual(response.status_code, 401)
