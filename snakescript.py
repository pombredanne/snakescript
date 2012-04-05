#!/usr/bin/env python

import ast
import _ast
import json
import sys
import os

MODULE_TEMPLATE = """$module("{name}", function() {{ with ({name}) {{

{body}

}}}})"""

CLASS_TEMPLATE = """\
$class(this, "{name}", [{bases}], function() {{

{body}

}})"""

DEF_TEMPLATE = """\
$def(this, "{name}", function({args}) {{
{body}
}})"""

FOR_TEMPLATE = """\
for (var $${target} = iter({iter}), {target} = next($${target}); {target} !== undefined; {target} = next($${target})){{
{body}
}}"""


BIN_OPS = {
	_ast.Add      : "({0} + {1})",
	_ast.Sub      : "({0} - {1})",
	_ast.Mult     : "({0} * {1})",
	_ast.Div      : "({0} / {1})",
	_ast.Mod      : "({0} % {1})",
	_ast.Pow      : "Math.pow({0}, {1})",
	_ast.LShift   : "({0} << {1})",
	_ast.RShift   : "({0} >> {1})",
	_ast.BitOr    : "({0} | {1})",
	_ast.BitXor   : "({0} ^ {1})",
	_ast.BitAnd   : "({0} & {1})",
	_ast.FloorDiv : "Math.floor({0}, {1})"
}

UNARY_OPS = {
	_ast.Not    : "(!({0}))"
}

CMP_OPS = {
	_ast.Eq    : "{0} === {1}",
	_ast.NotEq : "{0} !== {1}",
	_ast.Lt    : "{0} < {1}",
	_ast.LtE   : "{0} <= {1}",
	_ast.Gt    : "{0} > {1}",
	_ast.GtE   : "{0} >= {1}",
	_ast.Is    : "$is({0}, {1})",
	_ast.IsNot : "$isnot({0}, {1})",
	_ast.In    : "$in({0}, {1})",
	_ast.NotIn : "$notin({0}, {1})"
}

search_path = [
	os.path.join(sys.path[0], "lib"),
	os.path.join(sys.path[0], "test")
]

def is_private(name):
	return name.startswith("__") and not name.endswith("__")

class module(object):

	def __init__(self, name):
		self.name = name
		self.files = []
		for path in search_path:
			dpath = os.path.join(path, name)
			jpath = os.path.join(path, name + ".js")
			ppath = os.path.join(path, name + ".py")
			if os.path.isdir(dpath):
				for f in os.listdir(dpath):
					if f.endswith(".js") or f.endswith(".py"):
						self.files.append(os.path.join(dpath, f))
			if os.path.isfile(jpath):
				self.files.append(jpath)
			if os.path.isfile(ppath):
				self.files.append(ppath)

	def to_javascript(self):
		js = ""
		for f in self.files:
			src = open(f).read()
			if f.endswith(".js"):
				js += src
			elif f.endswith(".py"):
				js += _mod(ast.parse(src), self.name)
			else:
				raise TypeError
		return js

# takes block of code, indents once, rejoins and returns block
indent = lambda body: "\n".join(["    " + line for line in body.splitlines()])


def _unbracket(expr):
	"""
	Trim surrounding brackets
	"""
	if expr.startswith("(") and expr.endswith(")"):
		return _unbracket(expr[1:-1])
	else:
		return expr

def _blockstmt(keyword, expr, body):
	if expr:
		return "{kw} ({expr}) {{\n{body}\n}}".format(
			kw=keyword, expr=_unbracket(_expr(expr)),
			body=indent("\n".join(map(_stmt, body)))
		)
	else:
		return "{kw} {{\n{body}\n}}".format(
			kw=keyword, body=indent("\n".join(map(_stmt, body)))
		)

def _comment(a):
	return "/**\n * " + a + "\n */"

def _identifier(a):
	return a

def _int(a):
	return a

def _string(a):
	return json.dumps(a)

def _object(a):
	return json.dumps(a)

def _bool(a):
	return a

def _mod(a, name):
	if isinstance(a, _ast.Module):
		# $M
		return MODULE_TEMPLATE.format(
			body="\n".join(map(_stmt, a.body)),
			name=name
		)
	else:
		raise NotImplementedError(a)
	return script

def _stmt(a):
	if isinstance(a, _ast.FunctionDef):
		# $D
		script = DEF_TEMPLATE.format(
			name=_identifier(a.name),
			args=_arguments(a.args),
			body=indent("\n".join(map(_stmt, a.body)))
		)
	elif isinstance(a, _ast.ClassDef):
		# $C
		for node in ast.walk(a):
			node.class_name = a.name
		script = CLASS_TEMPLATE.format(
			name=_identifier(a.name),
			bases=", ".join(map(_expr, a.bases)),
			body=indent("\n".join(map(_stmt, a.body)))
		)
	elif isinstance(a, _ast.Return):
		if hasattr(a, "value"):
			script = "return " + _expr(a.value)
		else:
			script = "return"
	elif isinstance(a, _ast.Assign):
		if len(a.targets) == 1:
			script = "{0} = {1}".format(
				_expr(a.targets[0]),
				_expr(a.value)
			)
		else:
			script = "[{0}] = {1}".format(
				", ".join([_expr(t) for t in a.targets]),
				_expr(a.value)
			)
	elif isinstance(a, _ast.Print):
		# $P
		script = "print({0})".format(", ".join(map(_expr, a.values)))
	elif isinstance(a, _ast.For):
		script = FOR_TEMPLATE.format(
			target=_expr(a.target),
			iter=_expr(a.iter),
			body=indent("\n".join(map(_stmt, a.body)))
		)
	elif isinstance(a, _ast.If):
		script = _blockstmt("if", a.test, a.body)
		if a.orelse:
			script += "\n" + _blockstmt("else", None, a.orelse)
	elif isinstance(a, _ast.While):
		if a.orelse:
			script = "if (" + _unbracket(_expr(a.test)) + ") { " + \
			        _blockstmt("while", a.test, a.body) + "}\n" + \
			        _blockstmt("else", None, a.orelse)
		else:
			script = _blockstmt("while", a.test, a.body)
	elif isinstance(a, _ast.Raise):
		script = "throw " + _expr(a.type)
	elif isinstance(a, _ast.TryExcept):
		script = _blockstmt("try", None, a.body)
		for handler in a.handlers:
			script += "\n" + _excepthandler(handler)
	elif isinstance(a, _ast.TryFinally):
		script = _blockstmt("try", None, a.body) + \
		         _blockstmt("finally", None, a.finalbody)
	elif isinstance(a, _ast.Assert):
		# $A
		if a.msg:
			script = "$assert({0}, {1})".format(_expr(a.test), _expr(a.msg))
		else:
			script = "$assert({0})".format(_expr(a.test))
	elif isinstance(a, _ast.Import):
		# $I
		# TODO - check imported only once
		script = ""
		for name in a.names:
			script += module(_alias(name)).to_javascript()
	elif isinstance(a, _ast.Expr):
		if isinstance(a.value, _ast.Str):
			script = _comment(a.value.s)
		else:
			script = _expr(a.value)
	elif isinstance(a, _ast.Pass):
		return ""
	else:
		raise NotImplementedError(a)
	return script + ";"

def _expr(a):
	if a is None:
		script = "null"
	elif isinstance(a, _ast.BoolOp):
		if isinstance(a.op, _ast.And):
			script = "(" + " && ".join([_expr(value) for value in a.values]) + ")"
		elif isinstance(a.op, _ast.Or):
			script = "(" + " || ".join([_expr(value) for value in a.values]) + ")"
		else:
			raise NotImplementedError(a.op)
	elif isinstance(a, _ast.BinOp):
		try:
			script, args = BIN_OPS[type(a.op)], [
				_expr(a.left),
				_expr(a.right)
			]
		except KeyError:
			raise NotImplementedError(a.op)
	elif isinstance(a, _ast.UnaryOp):
		try:
			script, args = UNARY_OPS[type(a.op)], [
				_expr(a.operand)
			]
		except KeyError:
			raise NotImplementedError(a.op)
	elif isinstance(a, _ast.Dict):
		script, args = "{{{0}}}", [
			", ".join(_expr(a.keys[i]) + ": " + _expr(a.values[i]) for i in range(len(a.keys)))
		]
	elif isinstance(a, _ast.Compare):
		if len(a.ops) == 1:
			script, args = CMP_OPS[type(a.ops[0])], [
				_expr(a.left),
				_expr(a.comparators[0])
			]
		else:
			script = "({0})".format(
				" && ".join([
					CMP_OPS[type(a.ops[i])].format(js(a.left), _expr(a.comparators[i]))
					for i in range(len(a.ops))
				])
			)
	elif isinstance(a, _ast.Call):
		script, args = "{0}({1})", [
			_expr(a.func),
			", ".join([_expr(x) for x in a.args])
		]
	elif isinstance(a, _ast.Num):
		script = _object(a.n)
	elif isinstance(a, _ast.Str):
		script = _string(a.s)
	elif isinstance(a, _ast.Attribute):
		aname = a.attr
		script, args = "{0}.{1}", [
			_expr(a.value),
			_identifier(aname)
		]
	elif isinstance(a, _ast.Subscript):
		if isinstance(a.slice, _ast.Slice):
			script = "$getitem({0}, {1})"
		else:
			script = "{0}[{1}]"
		args = [_expr(a.value), _slice(a.slice)]
	elif isinstance(a, _ast.Name):
		script = _identifier(a.id)
	elif isinstance(a, _ast.List) or isinstance(a, _ast.Tuple):
		script, args = "[{0}]", [
			", ".join([_expr(x) for x in a.elts])
		]
	else:
		raise NotImplementedError(a)
	try:
		return script.format(*args)
	except NameError:
		return script

def _slice(a):
	if a is None:
		script = "null"
	elif isinstance(a, _ast.Slice):
		script, args = "slice({0}{1}{2})", [
			js(a.lower),
			", " + _expr(a.upper) if a.upper or a.step else "",
			", " + _expr(a.step) if a.step else ""
		]
	elif isinstance(a, _ast.Index):
		script = _expr(a.value)
	else:
		raise NotImplementedError(a)
	try:
		return script.format(*args)
	except NameError:
		return script

def _excepthandler(a):
	return _blockstmt("catch", a.type, a.body)

def _arguments(a):
	return ", ".join([_expr(x) for x in a.args])

def _alias(a):
	return a.name

if __name__ == "__main__":
	cmd = sys.argv.pop(0)
	for arg in sys.argv:
		print module(arg).to_javascript()

