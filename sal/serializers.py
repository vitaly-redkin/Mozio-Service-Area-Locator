from rest_framework import serializers

from sal.models import Provider, ServiceArea

"""
Seariazer for the Provider model
"""


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'name', 'email', 'phone', 'language', 'currency', )


"""
Seariazer for the ServiceArea model
"""


class ServiceAreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServiceArea
        fields = ('id', 'provider_id', 'name', 'price',
                  'polygon', 'x1', 'y1', 'x2', 'y2')
        # These fields are calculated ones and should not set with API
        read_only_fields = ('x1', 'y1', 'x2', 'y2')
