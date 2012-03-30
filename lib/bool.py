
assert (True and True) == True
assert (True and False) == False
assert (False and False) == False
assert (False and True) == False

assert (True or True) == True
assert (True or False) == True
assert (False or False) == False
assert (False or True) == True

assert (True and (False or True)) == True
assert ((True and False) or True) == True

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

