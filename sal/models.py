from django.db import models
import json

"""
Provider model

Defines an unique constraint for the provider name.
"""


class Provider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    currency = models.CharField(max_length=3)

    class Meta:
        ordering = ('name', )


"""
Service Area model

- Service area belongs to providers
- Defines an unique constraint for the provider and area name
- Area polygon is stored as a text field since GeoDjango and PostGIS not installed yet
- x1/y1/x2/y2 are basically calculated fields and represent a minimum bounding rectange (MBR) around the poligon outer circle
- There are four separate indexes for x1/y1/x2/y2 columns. They are used to do a primary filtering of service area.
- The valid polygon value looks like:
  {
    "type": "Polygon",
    "coordinates": [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ] ]
  }

"""


class ServiceArea(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    polygon = models.TextField()
    x1 = models.FloatField()
    y1 = models.FloatField()
    x2 = models.FloatField()
    y2 = models.FloatField()

    class Meta:
        unique_together = ('provider', 'name',)
        ordering = ('provider', 'name',)
        indexes = [
            models.Index(fields=['-x1']),
            models.Index(fields=['-y1']),
            models.Index(fields=['x2']),
            models.Index(fields=['y2']),
        ]

    """
    Overriden to set the area minimum bounding rectange (MBR) when area is saved
    """

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.set_mbr()
        super(ServiceArea, self).save(force_insert,
                                      force_update, using, update_fields)

    """
    Sets the area minimum bounding rectange (MBR)

    Parses polygon string (assuming it is JSON of the correct format).
    If something is wrong raises an exception.
    """

    def set_mbr(self):
        # Parse polygon as JSON
        try:
            parsedPolygon = json.loads(self.polygon)
        except Exception as e:
            raise Exception('Error parsing polygon JSON (%s): %s',
                            (self.polygon, e))

        if 'type' not in parsedPolygon:
            raise Exception(
                'Invalid polygon JSON (no type field): %s' % (self.polygon))
        type = parsedPolygon['type']
        if type != 'Polygon':
            raise Exception('Invalid polygon JSON type: %s' % (type))

        if 'coordinates' not in parsedPolygon:
            raise Exception(
                'Invalid polygon JSON (no array with coordinates): %s' % (self.polygon))
        coords = parsedPolygon['coordinates']
        if not isinstance(coords, list) or\
           not isinstance(coords[0], list) or\
           len(coords[0]) < 4:
            raise Exception('Polygon coordinates should be array \
                         with at least one array member \
                         with at least 4 points: %s' % (parsedPolygon))

        # Find min and max coordinates and set them to x1/y1/x2/y2
        outerCircle = coords[0]
        self.x1 = 180
        self.x2 = -180
        self.y1 = 180
        self.y2 = -180
        for coord in outerCircle:
            if not isinstance(coords, list) or len(coord) != 2:
                raise Exception(
                    'Invalid polygon JSON (one of coordinate array member is not a coordinate): %s' % (self.polygon))

            if coord[0] < self.x1:
                self.x1 = coord[0]
            if coord[1] < self.y1:
                self.y1 = coord[1]
            if coord[0] > self.x2:
                self.x2 = coord[0]
            if coord[1] > self.y2:
                self.y2 = coord[0]
