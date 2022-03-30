from pathlib import Path
from django.contrib.gis.gdal import DataSource
from core.models import Map, Layer, Site, Point

def load_populated_places(path):
    ds = DataSource(path)
    lyr = ds[0]

    m = Map.objects.create(name="Populated Places")
    l = Layer.objects.create(name="Cities", my_map=m)

    for feat in lyr:
        s = Site.objects.create(layer=l, name=feat.get("NAME"), data={"pop_max": feat.get("POP_MAX")})
        s._shape.add(Point(shape=feat.geom.wkt), bulk=False)



