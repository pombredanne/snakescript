import html
import unittest

print "hello, world"
print "hello, world".wrap("span")
print "hello, world".wrap("div", "greeting")

def foo():
	print "hello, foo"

foo()
foo()
foo()
foo()

record = {
	"person": {
		"name": "Nigel",
		"age": 35,
		"lovely": True,
		"details": {
			"height": "4m",
			"fav_colours": ["green", "brown"]
		}
	}
}

x=html(record, "record")
for i in range(2):
	for j in range(3):
		document.body.appendChild(x.cloneNode(True))
document.body.appendChild(html([1,2,3,4,5]))

