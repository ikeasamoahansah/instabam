from django.test import TestCase
from django.contrib.auth.models import User
from instabam.models import *

class TestModels(TestCase):
    
    def test_check_user_equals_profile(self):
        User.objects.create(username="Ike12", password="Ikeansah32", email="nyelorlom@gmail.com")
        user = User.objects.get(username="Ike12")
        userprofile = UserProfile.objects.get(user=user)
        self.assertEquals(user, userprofile.user)
    


