require(["esri/map",
         "esri/arcgis/utils", 
         "dojo/domReady!"
],
function(Map, arcgisUtils) {
    var deferred;

    arcgisUtils.arcgisUrl = "http://epedev005-ll:6080/arcgis/rest/services/hotec_larry/MapServer"
    deferred = arcgisUtils.createMap("hotec_larry", "mapDiv");
    
    deferred.then(function(reponse){
        map = response.map;
    });
});