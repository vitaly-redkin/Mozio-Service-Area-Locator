from django.views.generic import View
from django.http import JsonResponse
from django.core import serializers
from django.db import connection
from rest_framework import viewsets
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from sal.models import Provider, ServiceArea
from sal.serializers import ProviderSerializer, ServiceAreaSerializer


"""
ViewSet for the Provider model
"""


class ProviderViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


"""
ViewSet for the ServiceArea model
"""


class ServiceAreaViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.

    Valid polygon value looks like:
    {
      "type": "Polygon",
      "coordinates": [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ] ]
    }
    """
    serializer_class = ServiceAreaSerializer

    """
    Filters service areas to return the ones for the current provider only
    """

    def get_queryset(self):
        return ServiceArea.objects.filter(provider=self.kwargs['provider_pk'])

    """
    Sets the current provider when service area is created
    """

    def perform_create(self, serializer):
        serializer.save(provider=Provider.objects.get(
            pk=self.kwargs['provider_pk']))


"""
View for the Service Area locator
"""


class ServiceAreaLocatorView(View):
    """
    GET method

    Takes lat and lng as URL slugs
    """

    def get(self, request, *args, **kwargs):
        lat_s = kwargs['lat']
        lng_s = kwargs['lng']
        try:
            lat = float(lat_s)
            lng = float(lng_s)
        except Exception as e:
            raise Exception('Can\'t parse coordinates: (%s, %s)' %
                            (lat_s, lng_s))

        # Filter service areas to return only the ones with the given coordinates inside
        # Right now uses the area minimum bounding rectange (MBR) for filtering
        queryset = ServiceArea.objects\
            .filter(x1__lte=lat)\
            .filter(y1__lte=lng)\
            .filter(x2__gte=lat)\
            .filter(y2__gte=lng)\
            .select_related()\
            .values('provider__name', 'name', 'price', 'provider__currency')\
            .order_by('price')

        rows = []
        for item in list(queryset):
            row = {}
            row['provider_name'] = item['provider__name']
            row['area_name'] = item['name']
            row['price'] = float(item['price'])
            row['currency'] = item['provider__currency']
            rows.append(row)

        # print(connection.queries)

        return JsonResponse(rows, safe=False)
