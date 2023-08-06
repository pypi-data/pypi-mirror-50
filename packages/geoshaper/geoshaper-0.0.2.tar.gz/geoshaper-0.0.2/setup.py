from setuptools import setup

setup(
    name="geoshaper",
    version="0.0.2",
    description="An open source library to convert .shp files to GeoJSON/TopoJSON",
    url="http://github.com/Datawheel/geoshaper",
    download_url="http://github.com/Datawheel/geoshaper/archive/0.0.2.tar.gz",
    author="Carlos Navarrete",
    author_email="cnavarreteliz@gmail.com",
    license="MIT",
    packages=["geoshaper"],
    install_requires=[
        "fiona",
        "geopandas",
        "pandas",
        "shapely",
        "topojson"
    ],
    dependency_links=[
      "shapely",
      "git+ssh://git@https://github.com/calvinmetcalf/topojson.py.git#egg=0.1.01.dev0",
    ],
    keywords=["geojson", "topojson", "shapes"],
    zip_safe=True
)