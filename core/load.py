from pathlib import Path
from django.contrib.gis.gdal import DataSource
from core.models import Map, Layer, Site, Point, Line, Polygon

# Function that creates a map and one layer then loads
# shp data on this layer
def load_shape_data(path: str, map_name: str, layer_name: str, layer_data_key: str, site_name_key: str):
    ds = DataSource(path)
    lyr = ds[0]

    m = Map.objects.create(name=map_name)
    l = Layer.objects.create(name=layer_name, data_key=layer_data_key, my_map=m)

    for feat in lyr:
        s = Site.objects.create(layer=l, name=feat.get(site_name_key), data={layer_data_key: feat.get(layer_data_key)})
        geom_type = feat.geom.geom_type.name
        
        if (geom_type == 'Point'):
            s._shape.add(Point(shape=feat.geom.wkt), bulk=False)
        elif (geom_type == 'LineString'):
            s._shape.add(Line(shape=feat.geom.wkt), bulk=False)
        elif (geom_type == 'Polygon'):
            s._shape.add(Polygon(shape=feat.geom.wkt), bulk=False)


