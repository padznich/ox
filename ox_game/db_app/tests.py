from django.test import TestCase, Client

from models import Players

# Create your tests here.

class PageTests(TestCase):
    """Page tests."""
    def test_page_is_available(self):
        c = Client()
        response_admin = c.get('/')
        response_home = c.get('/home/')
        response_users = c.get('/users/')
        response_logs = c.get('/logs/')
        response_login = c.get('/login/')
        response_logout = c.get('/logout/')
        print('DEBUG admin', response_admin.__dict__)
        self.assertEquals(response_admin.status_int, 200)
        print('DEBUG home', response_home.__dict__)
        self.assertEquals(response_home.status_code, 200)
        print('DEBUG users', response_users)
        self.assertEquals(response_users.status_code, 200)
        self.assertEquals(response_logs.status_code, 200)
        self.assertEquals(response_login.status_code, 200)
        self.assertEquals(response_logout.status_code, 200)
