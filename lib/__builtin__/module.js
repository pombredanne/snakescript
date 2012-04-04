function $module(name, body) {

	function module(name, body) {
		this.__class__ = new type("module");
		this.__doc__ = "";
		this.__file__ = "";
		this.__name__ = name;
	}

	window[name] = new module(name, body);
	body.call(window[name]);

}
