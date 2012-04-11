
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


