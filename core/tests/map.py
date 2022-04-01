from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
from django.contrib.auth.models import User
from tastypie.models import ApiKey

from core.models import Map

class MapResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['maps.json']
    
    def setUp(self):
        super(MapResourceTest, self).setUp()

        self.username = 'testclient'
        self.api_key_string = 'testAPIkey'
        self.password = 'testpassword'
        self.user = User.objects.create_user(self.username, 'testclient@example.com', self.password)
        self.api_key = ApiKey.objects.create(user=self.user, key=self.api_key_string)

        self.map = Map.objects.get(name='Populated Places')
        self.map_data = {
            'name': 'Reefs',
            'description': 'Major coral reefs from WDB2'
        }

        self.map_list_url = '/api/v1/map/'
        self.map_detail_url = '/api/v1/map/{0}/'.format(self.map.pk)

    def get_credentials(self):
        return self.create_apikey(username=self.username, api_key=self.api_key_string)

    def test_get_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get(self.map_list_url, format='json'))

    def test_get_list_json(self):
        response = self.api_client.get(self.map_list_url, format='json', authentication=self.get_credentials())
        self.assertHttpOK(response)
        self.assertValidJSONResponse(response)
        objects = self.deserialize(response)['objects']
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0], {
            'description': self.map.description,
            'id': self.map.pk,
            'layers': list(self.map.layer_set.all()),
            'name': self.map.name,
            'resource_uri': self.map_detail_url
        })
    
    def test_get_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get(self.map_detail_url, format='json'))
    
    def test_get_detail_json(self):
        response = self.api_client.get(self.map_detail_url, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(response)

        self.assertKeys(self.deserialize(response), ['description', 'id', 'layers', 'name', 'resource_uri'])
        self.assertEqual(self.deserialize(response)['name'], self.map.name)
    
    def test_post_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.post(self.map_list_url, format='json', data=self.map_data))
    
    def test_post_list(self):
        self.assertEqual(Map.objects.count(), 1)
        self.assertHttpCreated(self.api_client.post(self.map_list_url, format='json', data=self.map_data, authentication=self.get_credentials()))
        self.assertEqual(Map.objects.count(), 2)
    
    def test_put_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.put(self.map_detail_url, format='json', data={}))

    def test_put_detail(self):
        original_data = self.deserialize(self.api_client.get(self.map_detail_url, format='json', authentication=self.get_credentials()))
        new_data = original_data.copy()
        new_data['name'] = 'Updated Map Title'
        new_data['description'] = 'Updated description'

        self.assertEqual(Map.objects.count(), 1)
        self.assertHttpAccepted(self.api_client.put(self.map_detail_url, format='json', data=new_data, authentication=self.get_credentials()))

        self.assertEqual(Map.objects.count(), 1)

        self.assertEqual(Map.objects.get(pk=self.map.pk).name, 'Updated Map Title')
        self.assertEqual(Map.objects.get(pk=self.map.pk).description, 'Updated description')

    def test_delete_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.map_detail_url, format='json'))
    
    def test_delete_detail(self):
        self.assertEqual(Map.objects.count(), 1)
        self.assertHttpAccepted(self.api_client.delete(self.map_detail_url, format='json', authentication=self.get_credentials()))
        self.assertEqual(Map.objects.count(), 0)