from django.contrib.gis.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from model_utils.managers import InheritanceManager

class Map(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

class Layer(models.Model):
    name = models.CharField(max_length=50)
    data_key = models.CharField(max_length=20)
    my_map = models.ForeignKey(Map, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Shape(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = InheritanceManager()

class Site(models.Model):
    name = models.CharField(max_length=100)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    data = models.JSONField()

    _shape = GenericRelation(Shape, content_type_field='content_type', object_id_field='object_id')

    @property
    def shape(self):
        ctype = ContentType.objects.get_for_model(self.__class__)
        try:
            shape_model = Shape.objects.all().select_subclasses().get(content_type=ctype, object_id=self.id)
            return shape_model.shape
        except:
            return None

    def __str__(self):
        return self.name

class Point(Shape):
    shape = models.PointField()

class Polygon(Shape):
    shape = models.PolygonField()

class MultiPolygon(Shape):
    shape = models.MultiPolygonField()

class Line(Shape):
    shape = models.LineStringField()