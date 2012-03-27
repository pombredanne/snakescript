
//tuple
function Tuple(i){for(var k in i){if(i.hasOwnProperty(k))this.push(i[k])}}
(function(P){
Tuple.prototype=Array.prototype
})(Tuple.prototype);

