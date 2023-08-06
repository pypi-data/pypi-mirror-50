# Setup and Installation
`pip install geoshaper`

An open source library to convert shape files to GeoJSON/TopoJSON

# Getting started
```
import geoshaper as gsh

shaper = gsh.GeoShaper("path")

shaper.to_topojson()

```

### geoshaper.GeoShaper(data="shapes")
data: folder path with shapes or GeoDataFrame object.
If data is a string, `GeoShaper` will read the folder, and will convert the shapes inside in a GeoDataFrame


#### shaper.to_geojson(path="output.json")
Save `shaper` to geojson. If `path` not provided, the result is returned as `output.json`.

#### shaper.to_topojson(path="output.json", quantization=1e6, simplify=0.0001)
Save `shaper` to geojson. If `path` not provided, the result is returned as `output.json`.


