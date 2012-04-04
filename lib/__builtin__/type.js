function type(obj) {

	if (this == window) {
		// called as function
		return obj.__class__;
	} else {
		// called as constructor
		this.__class__ = this;
		this.__name__ = obj;
		this.__str__ = function() {
			return type.__str__.call(this, this);
		}
		this.toString = this.__str__;
	}

}
type.__str__ = function(obj) {
	if (obj instanceof type) {
		return "<type '" + obj.__name__ + "'>";
	} else {
		return obj.toString();
	}
}

