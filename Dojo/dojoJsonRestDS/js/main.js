// using the class elsewhere...
require([
    "dojo/parser",
    "dojo/store/JsonRest",
    "dojo/domReady!"
  ],
  function (parser, JsonRest) {

    parser.parse();
    console.log("In dojoJsonRestDS/main.js");

    var data = new JsonRest({
      target: "http://www.arcgis.com/sharing/rest/content/items/2f5a28f82f4d41ec8dbe6cf96375a970/data",
    });

    //  data.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'};
    // {headers: {'Accept': 'application/json', 'Content-Type': 'application/json', 'Access-Control-Request-Headers': ''} });
    // {headers: {'Origin': 'localhost', 'X-Requested-With': ''} });

    // var data = new JsonRest( {target: "http://localhost:9000/jsonData.json", idProperty: "id"});

    // data.get().then( function(it) {
    //   it.forEach( a => console.log(`Got ${a.id}`) );
    // });

    data.query("").then(function (it) {
      it.forEach(a => console.log(`Got ${a.id}`));
    });
  });
