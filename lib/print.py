import html
import unittest

#assert 2+2==5

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
		print(x)
print(html([1,2,3,4,5]))

class MathTest:

	def test_addition_pass():
		assert 2 + 2 == 4

	def test_addition_fail():
		assert 2 + 2 == 5

	def test_addition_fail_with_msg():
		assert 2 + 2 == 5, "Can't do maths!"

	def test_multiple_addition_pass():
		assert 1 + 1 == 2
		assert 2 + 2 == 4
		assert 4 + 4 == 8

	def test_multiple_addition_fail_first():
		assert 1 + 1 == 3
		assert 2 + 2 == 4
		assert 4 + 4 == 8

	def test_multiple_addition_fail_last():
		assert 1 + 1 == 2
		assert 2 + 2 == 4
		assert 4 + 4 == 9

	def test_many_addition_pass():
		for i in range(1000000):
			assert 2 + 2 == 4

test(MathTest)

