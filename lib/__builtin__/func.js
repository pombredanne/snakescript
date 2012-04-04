
function $def(scope, name, func) {
	scope[name] = function() {
		return func.apply(this, list(arguments));
	};
	scope[name].__class__ = new type("function");
	scope[name].__name__ = name;
	if(scope.prototype) {
		scope.prototype[name] = function() {
			return func.apply(this, [this].concat(list(arguments)));
		}
		scope.prototype[name].__class__ = new type("instancemethod");
		scope.prototype[name].__name__ = name;
		if (name == "__str__") {
			scope.prototype.toString = scope.prototype.__str__;
		}
	}
	return func;
}

