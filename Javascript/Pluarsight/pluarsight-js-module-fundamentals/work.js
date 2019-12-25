// regular definition of function
console.log("***  function expression");
var f = function() {
    // private members
    var playerName = 'Larry L';
    
    function logPlayer() {
        console.log('The current player is ' + playerName + '.');
    }
};

f();  // executes and returns nothing! 
console.log(`playerName:  ${f.playerName}`);  // error:  not in scope!
f.logPlayer();  // error: not in scope!
console.log("*****");


// var f = function() {
//     // private members
//     var playerName = '';
    
//     function logPlayer() {
//         console.log('The current player is ' + playerName + '.');
//     }

//     return {
//         logPlayer: logPlayer,
//     }
// }();

// f.playerName = 'll';
// f.logPlayer();