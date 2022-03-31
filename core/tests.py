from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
from django.contrib.auth.models import User
from tastypie.models import ApiKey

class MapResourceTest(ResourceTestCaseMixin, TestCase):
    
    def setUp(self):
        super(MapResourceTest, self).setUp()

        self.username = 'testclient'
        self.api_key_string = 'testAPIkey'
        self.password = 'testpassword'
        self.user = User.objects.create_user(self.username, 'testclient@example.com', self.password)
        self.api_key = ApiKey.objects.create(user=self.user, key=self.api_key_string)

    def get_credentials(self):
        return self.create_apikey(username=self.username, api_key=self.api_key_string)

    def test_get_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/v1/map/'))

    def test_get_list_json(self):
        response = self.api_client.get('/api/v1/map/', format='json', authentication=self.get_credentials())
        self.assertHttpOK(response)
        self.assertValidJSONResponse(response)