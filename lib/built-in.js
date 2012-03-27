
StopIteration = function () {};
StopIteration.prototype = new Error();
StopIteration.name = 'StopIteration';
StopIteration.message = 'StopIteration';


/* Built-in Functions */
function abs(x){var y=Math.abs(x);if(isNaN(y))throw TypeError;else return y}
function all(x){for(var k in x){if(!x[k])return false}return true}
function any(x){for(var k in x){if(x[k])return true}return false}
function ascii(o){var x=str(o),s="";for(var i=0;i<x.length;i++){var c=x.charAt(i);s+=c>=" "&&c<="~"?c:"\\u"+ord(c).toString(16).rjust(4,"0")}return s}
function bin(x){return "0b"+x.toString(2)}
function bool(x){if(x==null||x==false||x==0||x==""||x==[]||(isinstance(x,Object)&&list(x).length==0))return false;else if(x.__bool__)return x.__bool__==true;else if(x.__len__)return x.__len__!=0;else return !!x}
//bytearray
//bytes
//callable
//chr
//classmethod
//compile
//complex
//delattr
function dict(obj){return new Dictionary(obj)}
//dir
function divmod(a,b){return tuple([Math.floor(a/b),a%b])}
//enumerate
//eval
//exec
//filter
function float() { /*TODO*/ }
//format
//frozenset
//getattr
//globals
//hasattr
//hash
//help
function hex(x){return "0x"+x.toString(16)}
//id
//input
function int() { /*TODO*/ }
function isinstance(obj, Class) {
	if (Class === undefined) {
		return obj === undefined
	} else if (Class === null) {
		return obj === null
	} else if (Class === Boolean || Class === bool) {
		return typeof obj == "boolean" || obj instanceof Boolean
	} else if (Class === Number || Class === int || Class === float) {
		var i = typeof obj == "number" || obj instanceof Number
		if (Class === int) i = i && obj == Math.floor(obj)
		return i
	} else if (Class === String || Class === str) {
		return typeof obj == "string" || obj instanceof String
	} else if (Class === Array || Class === list) {
		return obj instanceof Array
	} else if (Class === Function) {
		return typeof obj == "function" || obj instanceof Function
	} else if (Class === Object || Class === object) {
		return obj instanceof Object && !(obj instanceof Function) && !(obj instanceof Array) && !(obj instanceof String) && !(obj instanceof Number) && !(obj instanceof Boolean)
	} else {
		return obj instanceof Class
	}
}
//issubclass
function iter(o,s) {
	if(isinstance(o, Object)) {
		var values = []
		for(var x in o) {
			if(o.hasOwnProperty(x)) {
				values.push(x)
			}
		}
	} else {
		var values = o
	}
	var n = 0
	var N = function() {
		if (n < values.length) return values[n++]
		throw StopIteration
	}
	var i = {
		__iter__: function() { return i },
		__next__: N,
		next: N
	}
	return i
}
function len(s){if(s.__len__)return s.__len__();else if(s.length)return s.length;else return list(s).length}
function list(x){var L=[];{for(var k in x){if(x.hasOwnProperty(k))L.push(x[k])}};return L}
//locals
//map
//max
//memoryview
//min
function next(i,d){
	var x = i.__next__()
	if (x === undefined) return d
	else return x
}
function object(){return{}}
//oct
//open
function ord(c){if((typeof c=="string"||c instanceof String)&&c.length==1)return c.charCodeAt(0);else throw TypeError}
function pow(x,y,z){var n=Math.pow(x,y);return z==null?n:n%z}
function print(obj, sep, end) {
	end = end === undefined ? "\n" : end
	if (!isinstance(obj, Array)) obj = [obj]
	if (sep !== undefined) sep = document.createTextNode(sep)
	for (var i = 0; i < obj.length; i++) {
		if (sep !== undefined && i > 0) document.body.appendChild(sep.cloneNode(true))
		if (obj[i] instanceof Node) {
			document.body.appendChild(obj[i].cloneNode(true))
		} else {
			document.body.appendChild(document.createTextNode(str(obj[i])))
		}
	}
	document.body.appendChild(document.createTextNode(end))
}
//property
function range(x){var r=[];for(var i=0;i<x;i++)r.push(i);return r}
//repr
//reversed
//round
//set
//setattr
function slice(start,stop,step){return new Slice(start,stop,step)}
//sorted
//staticmethod
function str(x){return x.toString()}
//sum
//super
function tuple(iterable){return new Tuple(iterable)}
//type(x)
//vars
//zip

// misc, extra functions

function $extend(){
	var B = list(arguments), C = B.shift()
	for(var i = 0; i < B.length; i++) {
		for (var p in B[i]) {
			this[p] = B[i][p]
		}
	}
}
function $bind(o, n, f) {
	o[n] = f
	if(o.prototype) {
		o.prototype[n] = function() { return o[n].apply(this, [this].concat(list(arguments))) }
		if (n == "__str__") o.prototype.toString = o.prototype.__str__
	}
}
function $getitem(obj,i){
	if(isinstance(i, Slice)){
		var I=i.indices(obj.length),s=[];
		for(var x=I[0];x<I[1];x+=I[2]) {
			s.push(obj[x])
		}
		return s
	} else {
		return obj[i]
	}
}


