from django.urls import re_path,include, path
from tastypie.api import Api
from .api import MapResource, LayerResource, SiteResource, ShapeResource
from .views import index

v1_api = Api(api_name='v1')
v1_api.register(MapResource())
v1_api.register(LayerResource())
v1_api.register(SiteResource())
v1_api.register(ShapeResource())

urlpatterns = [
    path('', index, name="redirect"),
    re_path(r'^api/', include(v1_api.urls)),
]
