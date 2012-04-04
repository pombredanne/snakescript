
//string
(function(P){

P.wrap = function(t, c) {
	var F = document.createDocumentFragment(), e = document.createElement(t)
	if (c!=null) e.setAttribute("class", c)
	e.appendChild(document.createTextNode(this))
	F.appendChild(e)
	return F
}

})(String.prototype);


window.html = function(x,c) {
	var F=document.createDocumentFragment()
	if(isinstance(x,Object)||isinstance(x,Array)){
		var e=document.createElement("div")
		if(c!=null)e.setAttribute("class",c)
		if(isinstance(x,Array)) {
			for(i=0;i<x.length;i++)e.appendChild(html(x[i]))
		} else {
			for(i in x)e.appendChild(html(x[i],i))
		}
	} else {
		e=x.toString().wrap("span",c)
	}
	F.appendChild(e)
	return F
}

function write(obj, sep, end) {
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

