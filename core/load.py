from pathlib import Path
from django.contrib.gis.gdal import DataSource
from core.models import Map, Layer, MultiPolygon, Site, Point, Line, Polygon

# Function that creates a map and one layer then loads
# shp data on this layer
def load_shape_data(path: str, map_name: str, description: str, layer_name: str, layer_data_key: str, site_name_key: str):
    ds = DataSource(path)
    lyr = ds[0]

    m = Map.objects.create(name=map_name, description=description)
    l = Layer.objects.create(name=layer_name, data_key=layer_data_key, my_map=m)
    print("created map & layer")
    count = 0
    failed_features = []

    for feat in lyr:
        try:
            s = Site.objects.create(layer=l, name=feat.get(site_name_key), data={layer_data_key: feat.get(layer_data_key)})
            print("created site", s.name)
            geom_type = feat.geom.geom_type.name

            if (geom_type == 'Point'):
                s._shape.add(Point(shape=feat.geom.wkt), bulk=False)
            elif (geom_type == 'LineString'):
                s._shape.add(Line(shape=feat.geom.wkt), bulk=False)
            elif (geom_type == 'Polygon'):
                s._shape.add(Polygon(shape=feat.geom.wkt), bulk=False)
            elif (geom_type == 'MultiPolygon'):
                s._shape.add(MultiPolygon(shape=feat.geom.wkt), bulk=False)
            print("added shape", s.name, geom_type)
            count += 1
        except Exception as err:
            print("Encountered error {0} while loading feature {1}".format(err, feat.fid))
            failed_features.append(feat.fid)

    print("Created {0} sites, failed to load {1} features".format(count, len(failed_features)))


