

var map;
require(["esri/map",
         "esri/arcgis/utils",
         "dojo/domReady!"], function(Map, arcgisUtils)
{
    arcgisUtils.createMap(
        "016da65ef96e44019ee626a570836afe",
        "map").then(function(response) {
           map = response.map;
     });
});