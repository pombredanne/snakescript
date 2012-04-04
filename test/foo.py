msg = "hello, world"
print msg
print msg[5]
print msg[7:12]
document.writeln("<table border='1'><tr><td>" + msg + "</td></tr></table>")
document.writeln(10 + 3)
document.writeln(10 - 3)
document.writeln(10 * 3)
document.writeln(10 / 3)
document.writeln(10 % 3)
document.writeln(10 ** 3)
document.writeln(10 << 3)
document.writeln(10 >> 3)
document.writeln(10 | 3)
document.writeln(10 ^ 3)
document.writeln(10 & 3)
document.writeln(10 // 3)

a,b = [42,56]
print a
print "hello, \"world\" it's 10 o'clock"
nums = {"one": 1, "two": 2, "three": 3}
primes = [2,3,5,7,9]
primes.append(11)
print nums["two"]

class Person:

	def __init__(self, name, age):
		self.name = name
		self.age = age
	
	def __str__(self):
		return self.name + " is " + self.age + " years old"

class PrivatePerson(Person):

	def __init__(self, name, age):
		Person.__init__(self, name, age)

	def __doSomethingPrivate(self):
		print "ssh!"


nigel = PrivatePerson("Nigel", 35)
print str(nigel)

assert abs(42) == 42
assert abs(-42) == 42
assert abs(0) == 0

assert bool(None) == False
assert bool(False) == False
assert bool(0) == False
assert bool(0.0) == False
assert bool("") == False
assert bool([]) == False
assert bool({}) == False
assert bool(True) == True
assert bool(1) == True
assert bool(1.0) == True
assert bool("foo") == True
assert bool([1]) == True
assert bool({"foo":1}) == True

