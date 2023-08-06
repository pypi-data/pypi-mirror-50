try:
	# pylint: disable=no-name-in-module
	from collections.abc import Mapping
except ImportError:
	from collections import Mapping

class Row(dict):
	def __init__(self, items):
		dict.__init__(self, **dict(items))

	def __getitem__(self, k):
		return dict.__getitem__(self, k)

	def __getattr__(self, k):
		return dict.__getitem__(self, k)

	def __str__(self):
		return ', '.join([('%s=%' + 'rs'[str(i[1])==i[1]]) % i for i in dict.items(self)])

	def __repr__(self):
		return '<Row %s>' % self

	async def __aiter__(self):
		for item in dict.items(self):
			yield item
