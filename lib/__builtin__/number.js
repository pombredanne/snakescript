Number.__str__ = function(x) {
	return (x).toString();
}

Number.prototype.__class__ = new type("float");
Number.prototype.__str__ = Number.prototype.toString;

function int(x) {
	return parseInt(x);
}

function float(x) {
	return parseFloat(x);
}

