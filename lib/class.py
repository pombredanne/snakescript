
def __mangled_func():
	print "ehlol, ldrow"

def _private_func():
	print "hello, world"

def public_func():
	print "Hello, world!!"

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
assert nigel.name == "Nigel"
assert nigel.age == 35

