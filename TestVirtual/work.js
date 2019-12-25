 // But in this example, the variable assignment overrides the function declaration​​

var myName;



function myName () {
    console.log("Rich");
}
myName = "Richard";
console.log(typeof myName); // string

