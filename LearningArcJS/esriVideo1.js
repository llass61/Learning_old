require(["esri/map", "dojo/domReady!"],            
    function(Map) { 
        // map = new Map("map", {
        //     basemap: "topo",
        //     center: [-122.45, 37.75],
        //     zoom: 13
        // });

        // map = new esri.Map("mapDiv", {
        //     // extent: ((gs.state.lastExtent) ? gs.state.lastExtent : gs.conf.defaultExtent),
        //     basemap: "streets",
        //     infoWindow: new esri.dijit.Popup({}, dojo.create("div")),
        //     sliderPosition: "top-right",
        //     logo: false,
        //     fadeOnZoom: true,
        //     force3DTransforms: true,
        //     navigationMode: "css-transforms",
        //     optimizePanAnimation: true,
        //     // lods: gs.conf.lods,
        // });
        map = new Map("mapDiv", {
            basemap: "streets",
            center: [-56.049, 38.486],
            zoom: 3,
        });

    });





