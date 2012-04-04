
class EmptyClass(object):

	pass


class MyClass(object):

	class MyInnerClass(object):
	
		def __init__(self):
			pass

	def __init__(self, name):
		self.name = name

	def get_name(self):
		return self.name

class MySubClass(MyClass):

	def __init__(self, name, age):
		MyClass.__init__(self, name)
		self.age = age

	def get_age(self):
		return self.age

def my_func(name):
	return "hello, " + name

inst = EmptyClass()
assert EmptyClass.__class__.__name__ == "class"
assert inst.__class__.__name__ == "bigtest.EmptyClass"

inst = bigtest.EmptyClass()
assert bigtest.EmptyClass.__class__.__name__ == "class"
assert inst.__class__.__name__ == "bigtest.EmptyClass"

inst = MyClass("Bob")
assert MyClass.__class__.__name__ == "class"
assert MyClass.__init__.__class__.__name__ == "function"
assert MyClass.get_name.__class__.__name__ == "function"
assert MyClass.get_name(inst) == "Bob"
assert inst.__class__.__name__ == "bigtest.MyClass"
assert inst.__init__.__class__.__name__ == "instancemethod"
assert inst.get_name.__class__.__name__ == "instancemethod"
assert inst.get_name() == "Bob"
assert inst.name == "Bob"

inst = bigtest.MyClass("Bob")
assert bigtest.MyClass.__class__.__name__ == "class"
assert bigtest.MyClass.__init__.__class__.__name__ == "function"
assert bigtest.MyClass.get_name.__class__.__name__ == "function"
assert bigtest.MyClass.get_name(inst) == "Bob"
assert inst.__class__.__name__ == "bigtest.MyClass"
assert inst.__init__.__class__.__name__ == "instancemethod"
assert inst.get_name.__class__.__name__ == "instancemethod"
assert inst.get_name() == "Bob"
assert inst.name == "Bob"

inst = bigtest.MyClass.MyInnerClass()
assert bigtest.MyClass.MyInnerClass.__class__.__name__ == "class"
assert bigtest.MyClass.MyInnerClass.__init__.__class__.__name__ == "function"
assert inst.__class__.__name__ == "bigtest.MyClass.MyInnerClass"
assert inst.__init__.__class__.__name__ == "instancemethod"

inst = bigtest.MySubClass("Bob", 66)
assert bigtest.MySubClass.__class__.__name__ == "class"
assert bigtest.MySubClass.__init__.__class__.__name__ == "function"
assert bigtest.MySubClass.get_name.__class__.__name__ == "function"
assert bigtest.MySubClass.get_age.__class__.__name__ == "function"
assert bigtest.MySubClass.get_name(inst) == "Bob"
assert bigtest.MySubClass.get_age(inst) == 66
assert inst.__class__.__name__ == "bigtest.MySubClass"
assert inst.__init__.__class__.__name__ == "instancemethod"
assert inst.get_name.__class__.__name__ == "instancemethod"
assert inst.get_age.__class__.__name__ == "instancemethod"
assert inst.get_name() == "Bob"
assert inst.get_age() == 66
assert inst.name == "Bob"
assert inst.age == 66

assert my_func.__class__.__name__ == "function"
assert my_func("Bob") == "hello, Bob"

assert bigtest.my_func.__class__.__name__ == "function"
assert bigtest.my_func("Bob") == "hello, Bob"

