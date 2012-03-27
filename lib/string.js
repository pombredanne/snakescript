
//string
(function(P){

P.__add__ = P.concat;

P.__contains__ = function(s) {
	return this.indexOf(s) >= 0;
}


P.__getitem__ = function(item) {
	return $getitem(this, item).join("");
}

P.capitalize = function() {
	return this.charAt(0).toUpperCase() + this.substr(1);
}

P.center = function(width, fillchar) {
	var s = this + "";
	fillchar = fillchar || " ";
	var a = true;
	while (s.length < width) {
		s = a ? (s + fillchar) : (fillchar + s);
		a = !a;
	}
	return s;
}

P.join = function(seq) {
	return list(seq).join(this)
}

P.ljust = function(width, fillchar) {
	var s = this + "";
	fillchar = fillchar || " ";
	while (s.length < width) s += fillchar;
	return s;
}

P.rjust = function(width, fillchar) {
	var s = this + "";
	fillchar = fillchar || " ";
	while (s.length < width) s = fillchar + s;
	return s;
}

P.startswith = function(prefix) {
	return this.substr(0, prefix.length) == prefix
}

P.endswith = function(suffix) {
	return this.substr(-suffix.length) == suffix
}

})(String.prototype);

