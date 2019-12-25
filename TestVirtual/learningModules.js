
var globalVar = "a global variable";

// this will get evaluated since it is an expression
// due to the enclosing parens
(function() {
    // yes you can access globals!
    console.log("anonymous function1: " + globalVar);
}());

// instead of using globals, pass them in so it is not
// dependent on them
var gv = Object();

(function(one) {
    console.log("anonymous function2: " + one);
}("passed in global var"));

// another way of passing in globals
(function(gv){
    var pf = function() { console.log("private function") }

    gv.each = function(collection, iterator) {
    if (Array.isArray(collection)) {
      for (var i = 0; i < collection.length; i++) {
        iterator(collection[i], i, collection);
      }
    }
    else {
      for (var key in collection) {
        iterator(collection[key], key, collection);
      }
    }
  }
}(gv));
gv.each([1,2,3], function(a,b,c){console.log(a)});

// this is just a function - it is not evaluated
// you must call it to execute the method
function two() {
    console.log("function 2");
}

tmp = function() {
    var a = 4;
    console.log("anonymous function3")
};

tmp()

