
//dict
function Dictionary(obj){for(var k in obj){if(obj.hasOwnProperty(k))this[k]=obj[k]}}
(function(P){
P.update=function(x){for (var i in x) this[i] = x[i]}
})(Dictionary.prototype);

