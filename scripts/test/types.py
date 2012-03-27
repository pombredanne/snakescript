
objects = [
	{},
	{"foo":1},
	{foo:1},
	{foo:1,length:2},
	Object()
]

arrays = [
	[],
	[3,4,5,6],
	["foo","bar"],
	["blah",10,true],
	Array()
]

for x in objects:
	console.log(x)
	assert isinstance(x, object) == True
	assert isinstance(x, list) == False

for x in arrays:
	console.log(x)
	assert isinstance(x, object) == False
	assert isinstance(x, list) == True

