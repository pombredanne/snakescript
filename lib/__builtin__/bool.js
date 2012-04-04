var True = true, False = false, None = null;

Boolean.__str__ = function(x) {
	return x ? "True" : "False";
}

Boolean.prototype.__class__ = new type("bool");
Boolean.prototype.__str__ = function() {
	return this ? "True" : "False";
}
Boolean.prototype.toString = Boolean.prototype.__str__;

function bool(x) { 
	if (x == null || x == false || x == 0 || x == "" || x == [] || (isinstance(x,Object) && list(x).length == 0)) {
		return false;
	} else if (x.__bool__) {
		return x.__bool__ == true;
	} else if (x.__len__) {
		return x.__len__ != 0;
	} else {
		return !!x;
	}
}

