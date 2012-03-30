function $assert(test, msg) {
	if (!test) {
		if (msg === undefined) msg = "";
		throw msg
	}
}

window.test = function(Class) {

	function testMethod(Class, method) {
		function cell(text, style) {
			var c = document.createElement("td");
			c.setAttribute("style", "border:1px solid #333;" + style);
			c.appendChild(document.createTextNode(text));
			return c;
		}
		var inst = new Class();
		var e;
		var t0 = new Date();
		try {
			inst[method].call();
			e1 = "PASS"
		} catch(ex) {
			e1 = "FAIL"
			if (ex) {
				e1 += " (" + ex.toString() + ")"
			}
		}
		var t1 = new Date();
		var frag = document.createDocumentFragment(),
		    row = document.createElement("tr");
		row.appendChild(cell(t0.getTime()));
		row.appendChild(cell(method));
		row.appendChild(cell((t1.getTime() - t0.getTime()) + "ms", "text-align:right;"));
		row.appendChild(cell(e1, e1=="PASS"?"background-color:green;color:white;":"background-color:red;color:white;"));
		frag.appendChild(row);
		return frag;
	}

	var frag = document.createDocumentFragment();
	var table = document.createElement("table");
	table.setAttribute("style", "border-collapse:collapse;border:1px solid #333;");
	var tbody = document.createElement("tbody");
	for (var fn in Class.prototype) {
		if (Class.prototype[fn] instanceof Function) {
			tbody.appendChild(testMethod(Class, fn));
		}
	}
	table.appendChild(tbody);
	frag.appendChild(table);
	document.body.appendChild(frag);

}
