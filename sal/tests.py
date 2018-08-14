from django.urls import include, path, reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
import json 

from sal.models import Provider, ServiceArea


"""
Provider API Tests
"""
class TestUtils:
    @staticmethod
    def create_providers(test_case):
        ids = []
        for i in range(1, 6):
            provider_count = Provider.objects.count()

            url = '/providers/'

            data = {
                "name": "Provider " + str(i),
                "email": "test@test.com",
                "phone": "111",
                "currency": "USD",
                "language": "English"
            }
            response = test_case.client.post(url, data, format='json')

            test_case.assertEqual(response.status_code, status.HTTP_201_CREATED)
            test_case.assertEqual(Provider.objects.count(), provider_count + 1)
            id = response.data['id']
            ids.append(id)
            test_case.assertEqual(Provider.objects.get(pk=id).name, data['name'])

        return ids

    @staticmethod
    def create_service_areas(test_case):
        provider_ids = TestUtils.create_providers(test_case)
        provider_id = provider_ids[0]

        ids = []

        for i in range(1, 6):
            service_area_count = ServiceArea.objects.count()

            coords = []    
            for j in range(0, 5):
                x = (0 if j == 0 else 1 if j == 1 else 1 if j == 2 else 0 if j == 3 else 0) * 10 + i
                y = (0 if j == 0 else 0 if j == 1 else 1 if j == 2 else 1 if j == 3 else 0) * 10 + i
                point = [x, y]
                coords.append(point)
            polygon = json.dumps({'type': 'Polygon', 'coordinates': [coords,]})

            url = '/providers/%s/serviceareas/' % (provider_id)
            data = {
                "name": "Area " + str(i),
                "price": i * 100,
                "polygon": polygon
            }
            response = test_case.client.post(url, data, format='json')

            test_case.assertEqual(response.status_code, status.HTTP_201_CREATED)
            test_case.assertEqual(ServiceArea.objects.count(), service_area_count + 1)
            id = response.data['id']
            ids.append(id)
            service_area = ServiceArea.objects.get(pk=id)
            test_case.assertEqual(service_area.name, data['name'])
            test_case.assertEqual(service_area.name, data['name'])
            test_case.assertEqual(service_area.x1, i)
            test_case.assertEqual(service_area.y1, i)
            test_case.assertEqual(service_area.x2, 10 + i)
            test_case.assertEqual(service_area.y2, 10 + i)

        return ids



class ProviderTest(APITestCase):
    """
    Provider creation test
    """

    def test_create(self):
        TestUtils.create_providers(self)

    """
    Provider list test
    """

    def test_list(self):
        url = '/providers/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        providers = response.data
        self.assertEqual(Provider.objects.count(), len(providers))

        ids = TestUtils.create_providers(self)
        self.assertEqual(Provider.objects.count(), len(ids))
        self.assertGreater(len(ids), 0)

        response = self.client.get(url)
        providers = response.data
        self.assertEqual(providers[0]['name'], 'Provider 1')

    """
    Provider detail test
    """

    def test_detail(self):
        ids = TestUtils.create_providers(self)
        id = ids[0]

        url = '/providers/%s/' % (id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['id'], id)
        self.assertEqual(Provider.objects.get(pk=id).name, data['name'])

    """
    Provider update test
    """

    def test_put(self):
        ids = TestUtils.create_providers(self)
        id = ids[0]
        provider = Provider.objects.get(pk=id)

        url = '/providers/%s/' % (id)
        data = {
            "name": provider.name,
            "email": provider.email,
            "phone": "222",
            "currency": provider.currency,
            "language": provider.language
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Provider.objects.get(pk=id).name, data['name'])
        self.assertEqual(Provider.objects.get(pk=id).phone, data['phone'])

    """
    Provider partial update test
    """

    def test_patch(self):
        ids = TestUtils.create_providers(self)
        id = ids[0]
        provider = Provider.objects.get(pk=id)

        url = '/providers/%s/' % (id)
        data = {
            "phone": "333",
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Provider.objects.get(pk=id).name, provider.name)
        self.assertEqual(Provider.objects.get(pk=id).phone, data['phone'])

    """
    Provider delete test
    """

    def test_delete(self):
        ids = TestUtils.create_providers(self)
        id = ids[len(ids) - 1]
        provider = Provider.objects.get(pk=id)

        url = '/providers/%s/' % (id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Provider.objects.filter(pk=id).count(), 0)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


"""
Service Area API Tests
"""


class ServiceAreaTest(APITestCase):
    """
    Service Area creation test
    """

    def test_create(self):
        TestUtils.create_service_areas(self)


    """
    Service Area list test
    """

    def test_list(self):
        service_area_ids = TestUtils.create_service_areas(self)
        service_area = ServiceArea.objects.get(pk=service_area_ids[0])
        provider_id = service_area.provider.id
        self.assertEqual(ServiceArea.objects.filter(provider=provider_id).count(), len(service_area_ids))
        self.assertGreater(len(service_area_ids), 0)

        url = '/providers/%s/serviceareas/' % (provider_id)
        response = self.client.get(url)
        service_areas = response.data
        self.assertEqual(service_areas[0]['name'], 'Area 1')


    """
    Service Area detail test
    """

    def test_detail(self):
        service_area_ids = TestUtils.create_service_areas(self)
        service_area_id = service_area_ids[0]
        service_area = ServiceArea.objects.get(pk=service_area_id)
        provider_id = service_area.provider.id

        url = '/providers/%s/serviceareas/%s/' % (provider_id, service_area_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['id'], service_area_id)
        self.assertEqual(ServiceArea.objects.get(pk=service_area_id).name, data['name'])


    """
    Service Area update test
    """

    def test_put(self):
        service_area_ids = TestUtils.create_service_areas(self)
        service_area_id = service_area_ids[0]
        service_area = ServiceArea.objects.get(pk=service_area_id)
        provider_id = service_area.provider.id

        url = '/providers/%s/serviceareas/%s/' % (provider_id, service_area_id)
        data = {
            "name": service_area.name,
            "price": 111,
            "polygon": service_area.polygon
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ServiceArea.objects.get(pk=service_area_id).name, data['name'])
        self.assertEqual(ServiceArea.objects.get(pk=service_area_id).price, data['price'])


    """
    Service Area partial update test
    """

    def test_put(self):
        service_area_ids = TestUtils.create_service_areas(self)
        service_area_id = service_area_ids[0]
        service_area = ServiceArea.objects.get(pk=service_area_id)
        provider_id = service_area.provider.id

        url = '/providers/%s/serviceareas/%s/' % (provider_id, service_area_id)
        data = {
            "price": 999,
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ServiceArea.objects.get(pk=service_area_id).name, service_area.name)
        self.assertEqual(ServiceArea.objects.get(pk=service_area_id).price, data['price'])



    """
    Service Area delete test
    """

    def test_delete(self):
        service_area_ids = TestUtils.create_service_areas(self)
        service_area_id = service_area_ids[0]
        service_area = ServiceArea.objects.get(pk=service_area_id)
        provider_id = service_area.provider.id

        url = '/providers/%s/serviceareas/%s/' % (provider_id, service_area_id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ServiceArea.objects.filter(pk=service_area_id).count(), 0)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


"""
Service Area Locator API Tests
"""


class ServiceAreaLocatorTest(APITestCase):
    """
    Service Area Locator list test
    """
    def test_list(self):
        service_area_ids = TestUtils.create_service_areas(self)

        test_cases = [
          { 'expected_count': 1, 'point': {'lat': 1, 'lng': 1} },
          { 'expected_count': 5, 'point': {'lat': 10, 'lng': 10} },
          { 'expected_count': 0, 'point': {'lat': -10, 'lng': 10} },
        ]
        for test_case in test_cases:
            expected_count = test_case['expected_count']
            point = test_case['point']
            url = reverse('locator', kwargs=point)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            self.assertEqual(len(data), expected_count)
            pass

