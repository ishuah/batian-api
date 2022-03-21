from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
from tastypie.authentication import ApiKeyAuthentication
from .models import *
from tastypie.resources import ALL_WITH_RELATIONS


class MapResource(ModelResource):
    class Meta:
        queryset = Map.objects.all()
        resource_name = 'map'
        authentication = ApiKeyAuthentication()

class LayerResource(ModelResource):
    class Meta:
        queryset = Layer.objects.all()
        resource_name = 'layer'
        authentication = ApiKeyAuthentication()

class SiteResource(ModelResource):
    shapes = fields.ToManyField('core.api.ShapeResource', '_shape', null=True, blank=True, full_detail=True, full=True)
    class Meta:
        queryset = Site.objects.all()
        resource_name = 'site'
        authentication = ApiKeyAuthentication()

class ShapeResource(ModelResource):
    content_object = GenericForeignKeyField({
        Site: SiteResource,
    }, 'content_object', null=True, blank=True)

    class Meta:
        queryset = Shape.objects.all()
        resource_name = 'shape'
        authentication = ApiKeyAuthentication()

    def dehydrate(self, bundle):
        obj = Shape.objects.filter(pk=bundle.data["id"]).select_subclasses()[0]
        if not obj:
            obj = bundle.obj
        if obj:
            geom_resource = self.chooseResource(obj)
            new_bundle = geom_resource.build_bundle(obj=obj)
            bundle = geom_resource.full_dehydrate(new_bundle)
        return bundle

    def chooseResource(self, GeomModel):
        if GeomModel.__class__.__name__ == "Point":
            return PointResource()
        elif GeomModel.__class__.__name__ == "Polygon":
            return PolygonResource()
        elif GeomModel.__class__.__name__ == "MultiPolygon":
            return MultiPolygonResource()

class PointResource(ShapeResource):
    class Meta:
        queryset = Point.objects.all()
        authentication = ApiKeyAuthentication()

    def dehydrate(self, bundle):
        return bundle

class PolygonResource(ShapeResource):
    class Meta:
        queryset = Polygon.objects.all()
        authentication = ApiKeyAuthentication()

    def dehydrate(self, bundle):
        return bundle

class MultiPolygonResource(ShapeResource):
    class Meta:
        queryset = MultiPolygon.objects.all()
        authentication = ApiKeyAuthentication()

    def dehydrate(self, bundle):
        return bundle