from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from instabam.views import *
import uuid


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    # def test_login_url_resolves(self):
    #     url = reverse('login')
    #     self.assertEquals(resolve(url).func.view_class, login)

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, signup)

    # def test_logout_url_resolves(self):
    #     url = reverse('logout')
    #     self.assertEquals(resolve(url).func.view_class, logout_view)

    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, search)

    def test_post_url_resolves(self):
        url = reverse('post')
        self.assertEquals(resolve(url).func, post_content)

    def test_profile_url_resolves(self):
        url = reverse('profile', args=['1'])
        self.assertEquals(resolve(url).func, profile)

    def test_update_user_url_resolves(self):
        url = reverse('update_user')
        self.assertEquals(resolve(url).func, update_user)



class UUIDViewTestCase(TestCase):

    test_uuid = uuid.uuid4()

    def test_view_post_url_resolves(self):
        url = reverse('view_post', args=[self.test_uuid])
        self.assertEquals(resolve(url).func, view_post)


    def test_reply_url_resolves(self):
        url = reverse('reply', args=[self.test_uuid])
        self.assertEquals(resolve(url).func, reply)
