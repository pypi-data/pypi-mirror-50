try:
	# pylint: disable=no-name-in-module
	from collections.abc import Mapping
except ImportError:
	from collections import Mapping

class Row(dict):
	SPECIAL = ['name', 'type']

	def __init__(self, items):
		dict.__init__(self, **dict(items))

	def __getitem__(self, k):
		return dict.__getitem__(self, k)

	def __getattr__(self, k):
		return dict.__getitem__(self, k)

	def __str__(self):
		string = ''
		for col in Row.SPECIAL:
			if col in self:
				string = '%s %s' % (self[col], string)
		attrs = ''
		for col, value in self:
			if col not in Row.SPECIAL:
				attrs = '%s%s=%r, ' % (attrs, col, value)
		if len(attrs):
			string = '%s(%s)' % (string, attrs.rstrip(', '))
		return string.rstrip()

	def __repr__(self):
		return '<%s>' % self

	def __iter__(self):
		for item in dict.items(self):
			yield item

	async def __aiter__(self):
		for item in self:
			yield item
