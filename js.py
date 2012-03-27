#!/usr/bin/env python

import ast
import _ast
import json

from flask import Flask, make_response, url_for
app = Flask(__name__)

MODULE_TEMPLATE = """(function(self){{
{body}
}})(window);"""

CLASS_TEMPLATE = """\
self.{name} = function {name}() {{
    i = "__init__"
    if (this == window) {{
        // factory
        I = new {name}()
        if (I[i]) I[i].apply(I, arguments)
        return I
    }} else {{
        // constructor
        P = {name}.prototype
        if (P[i]) P[i].apply(this, arguments)
    }}
}}
{subclasses}
{body}
"""

METHOD_TEMPLATE = """\
$bind({class_name}, "{name}", function({args}) {{
{body}
}})
"""

PRIVATE_FUNCTION_TEMPLATE = """\
function {name}({args}) {{
{body}
}}

"""

PUBLIC_FUNCTION_TEMPLATE = """\
function {name}({args}) {{
{body}
}}

"""

FOR_TEMPLATE = """\
try{{for(var ${target}=iter({iter}),{target}=next(${target});;{target}=next(${target})){{
{body}
}}}}catch(e){{if(e!=StopIteration)throw e;}}
"""

BIN_OPS = {
	_ast.Add      : "{0}+{1}",
	_ast.Sub      : "{0}-{1}",
	_ast.Mult     : "{0}*{1}",
	_ast.Div      : "{0}/{1}",
	_ast.Mod      : "{0}%{1}",
	_ast.Pow      : "Math.pow({0},{1})",
	_ast.LShift   : "{0}<<{1}",
	_ast.RShift   : "{0}>>{1}",
	_ast.BitOr    : "{0}|{1}",
	_ast.BitXor   : "{0}^{1}",
	_ast.BitAnd   : "{0}&{1}",
	_ast.FloorDiv : "Math.floor({0},{1})"
}

CMP_OPS = {
	_ast.Eq    : "{0}==={1}",
	_ast.NotEq : "{0}!=={1}",
	_ast.Lt    : "{0}<{1}",
	_ast.LtE   : "{0}<={1}",
	_ast.Gt    : "{0}>{1}",
	_ast.GtE   : "{0}>={1}"
}

def is_private(name):
	return name.startswith("__") and not name.endswith("__")

@app.route("/py")
def py():
	py = ""
	py += open("lib/built-in.js").read()
	py += open("lib/slice.js").read()
	py += open("lib/tuple.js").read()
	py += open("lib/dict.js").read()
	py += open("lib/array.js").read()
	py += open("lib/string.js").read()
	py += open("modules/html.js").read()
	return py

@app.route("/test/<path:file_name>")
def other(file_name):
	return """\
<html>
<head>
</head>
<body>
<script src="/py"></script>
<script src="/scripts/test/{0}.py"></script>
</body>
</html>
""".format(file_name)

@app.route("/scripts/<path:file_name>")
def py2js(file_name):
	fin = file("scripts/{0}".format(file_name))
	a = ast.parse(fin.read())
	rs = make_response(js(a))
	rs.headers["Content-Type"] = "application/json"
	return rs

def js(a):
	if a is None:
		script = "null"
	elif isinstance(a, _ast.Module):
		script = MODULE_TEMPLATE.format(
			body="\n".join(map(js, a.body))
		)
	elif isinstance(a, _ast.FunctionDef):
		if hasattr(a, "class_name"):
			template = METHOD_TEMPLATE
		elif is_private(a.name):
			template = PRIVATE_FUNCTION_TEMPLATE
		else:
			template = PUBLIC_FUNCTION_TEMPLATE
		script = template.format(
			class_name=a.class_name if hasattr(a, "class_name") else None,
			name=a.name,
			args=js(a.args),
			body="\n".join(map(js, a.body))
		)
	elif isinstance(a, _ast.ClassDef):
		for node in ast.walk(a):
			node.class_name = a.name
		script = CLASS_TEMPLATE.format(
			name=a.name,
			subclasses="\n".join(["$extend({C},{B})\n".format(C=a.name, B=js(b)) for b in a.bases]),
			body="\n".join(map(js, a.body))
		)
	elif isinstance(a, _ast.Return):
		script, args = "return {0}", [js(a.value)]
	elif isinstance(a, _ast.Assign):
		if len(a.targets) == 1:
			script, args = "{0}={1}", [
				js(a.targets[0]),
				js(a.value)
			]
		else:
			script, args = "[{0}]={1}", [
				", ".join([js(t) for t in a.targets]),
				js(a.value)
			]
	elif isinstance(a, _ast.Print):
		script, args = "print({0})", [
			",".join(map(js, a.values))
		]
	elif isinstance(a, _ast.For):
		script = FOR_TEMPLATE.format(
			target=js(a.target),
			iter=js(a.iter),
			body="\n".join(map(js, a.body))
		)
	elif isinstance(a, _ast.Assert):
		if a.msg:
			script, args = "console.assert({0}, {1})", [
				js(a.test),
				js(a.msg)
			]
		else:
			script, args = "console.assert({0})", [
				js(a.test)
			]
	elif isinstance(a, _ast.Expr):
		script = js(a.value)
	elif isinstance(a, _ast.Pass):
		script = ""
	elif isinstance(a, _ast.BoolOp):
		if isinstance(a.op, _ast.And):
			script = "(" + "&&".join([js(value) for value in a.values]) + ")"
		elif isinstance(a.op, _ast.Or):
			script = "(" + "||".join([js(value) for value in a.values]) + ")"
		else:
			raise NotImplementedError(a.op)
	elif isinstance(a, _ast.BinOp):
		try:
			script, args = "(" + BIN_OPS[type(a.op)] + ")", [
				js(a.left),
				js(a.right)
			]
		except KeyError:
			raise NotImplementedError(a.op)
	elif isinstance(a, _ast.Dict):
		script, args = "{{{0}}}", [
			",".join(js(a.keys[i]) + ":" + js(a.values[i]) for i in range(len(a.keys)))
		]
	elif isinstance(a, _ast.Compare):
		if len(a.ops) == 1:
			script, args = CMP_OPS[type(a.ops[0])], [
				js(a.left),
				js(a.comparators[0])
			]
		else:
			script = "({0})".format(
				" && ".join([
					CMP_OPS[type(a.ops[i])].format(js(a.left), js(a.comparators[i]))
					for i in range(len(a.ops))
				])
			)
	elif isinstance(a, _ast.Call):
		script, args = "{0}({1})", [
			js(a.func),
			",".join([js(x) for x in a.args])
		]
	elif isinstance(a, _ast.Num):
		script = json.dumps(a.n)
	elif isinstance(a, _ast.Str):
		script = json.dumps(a.s)
	elif isinstance(a, _ast.Attribute):
		if a.attr == "__class__":
			aname = "__proto__"
		else:
			aname = a.attr
		script, args = "{0}.{1}", [
			js(a.value),
			aname
		]
	elif isinstance(a, _ast.Subscript):
		if isinstance(a.slice, _ast.Slice):
			script = "{0}.__getitem__({1})"
		else:
			script = "{0}[{1}]"
		args = [js(a.value), js(a.slice)]
	elif isinstance(a, _ast.Name):
		if a.id == "None":
			script = "null"
		elif a.id == "True":
			script = "true"
		elif a.id == "False":
			script = "false"
		else:
			script = a.id
	elif isinstance(a, _ast.List) or isinstance(a, _ast.Tuple):
		script, args = "[{0}]", [
			",".join([js(x) for x in a.elts])
		]
	elif isinstance(a, _ast.Slice):
		script, args = "slice({0}{1}{2})", [
			js(a.lower),
			"," + js(a.upper) if a.upper or a.step else "",
			"," + js(a.step) if a.step else ""
		]
	elif isinstance(a, _ast.Index):
		script = js(a.value)
	elif isinstance(a, _ast.arguments):
		script = ",".join([js(x) for x in a.args])
	else:
		raise NotImplementedError(a)
	try:
		return script.format(*args)
	except NameError:
		return script

if __name__ == "__main__":
	app.run(debug=True)

