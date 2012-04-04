

class TestCase:

	def fail(self, msg=None):
		"""Fail immediately, with the given message."""
		raise {"name": "Assertion Failure"}, msg

	def assertFalse(self, expr, msg=None):
		"Fail the test if the expression is true."
		if expr:
			raise {"name": "Assertion Failure"}, msg

	def assertTrue(self, expr, msg=None):
		"""Fail the test unless the expression is true."""
		if not expr:
			raise {"name": "Assertion Failure"}, msg

	def assertRaises(self, excClass, callableObj, *args, **kwargs):
		"""Fail unless an exception of class excClass is thrown
		   by callableObj when invoked with arguments args and keyword
		   arguments kwargs. If a different type of exception is
		   thrown, it will not be caught, and the test case will be
		   deemed to have suffered an error, exactly as for an
		   unexpected exception.
		"""
		try:
			callableObj(*args, **kwargs)
		except excClass:
			return
		else:
			if hasattr(excClass,'__name__'):
				excName = excClass.__name__
			else:
				excName = str(excClass)
			raise {"name": "Assertion Failure"}, "%s not raised" % excName

	def assertEqual(self, first, second, msg=None):
		"""Fail if the two objects are unequal as determined by the '=='
		   operator.
		"""
		if not first == second:
			raise {"name": "Assertion Failure"}, \
				  (msg or '%r != %r' % (first, second))

	def assertNotEqual(self, first, second, msg=None):
		"""Fail if the two objects are equal as determined by the '=='
		   operator.
		"""
		if first == second:
			raise {"name": "Assertion Failure"}, \
				  (msg or '%r == %r' % (first, second))

	def assertAlmostEqual(self, first, second, places=7, msg=None):
		"""Fail if the two objects are unequal as determined by their
		   difference rounded to the given number of decimal places
		   (default 7) and comparing to zero.

		   Note that decimal places (from zero) are usually not the same
		   as significant digits (measured from the most signficant digit).
		"""
		if round(abs(second-first), places) != 0:
			raise {"name": "Assertion Failure"}, \
				  (msg or '%r != %r within %r places' % (first, second, places))

	def assertNotAlmostEqual(self, first, second, places=7, msg=None):
		"""Fail if the two objects are equal as determined by their
		   difference rounded to the given number of decimal places
		   (default 7) and comparing to zero.

		   Note that decimal places (from zero) are usually not the same
		   as significant digits (measured from the most signficant digit).
		"""
		if round(abs(second-first), places) == 0:
			raise {"name": "Assertion Failure"}, \
				  (msg or '%r == %r within %r places' % (first, second, places))

