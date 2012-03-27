
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


function html(x,c) {
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

