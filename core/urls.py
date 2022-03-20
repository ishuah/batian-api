from django.urls import re_path,include
from tastypie.api import Api
from .api import *

v1_api = Api(api_name='v1')
v1_api.register(MapResource())
v1_api.register(LayerResource())
v1_api.register(SiteResource())
v1_api.register(ShapeResource())

urlpatterns = [
    re_path(r'^api/', include(v1_api.urls)),
]
