function $class(scope, name, bases, body) {
    // build constructor
    scope[name] = function() {
        if (this == scope) {
            var inst = new scope[name]();
            inst.__class__ = new type([scope.__name__, name].join("."));
            if (inst.__init__) {
            	inst.__init__.apply(inst, arguments);
            }
            return inst;
        } else {
            //var proto = scope[name].prototype;
            //if (proto["__init__"]) {
            //	proto["__init__"].apply(this, arguments);
            //}
        }
    }
    self = scope[name];
    self.__class__ = new type("class");
    self.__name__ = [scope.__name__, name].join(".");
    // extend from base classes
    if (bases) {
	    for (var i = 0; i < bases.length; i++) {
	        var base = bases[i];
	        for (var prop in base) {
	            self[prop] = base[prop];
	        }
	        for (var prop in base.prototype) {
	            self.prototype[prop] = base.prototype[prop];
	        }
	    }
    }
    // execute body
    body.call(self, self);
}

