try:
	# pylint: disable=no-name-in-module
	from collections.abc import Mapping
except ImportError:
	from collections import Mapping

class Row(dict):
	def __init__(self, items):
		super().__init__(self, **items)

	def __getitem__(self, k):
		return super().__getitem__(self, k)

	def __getattr__(self, k):
		return super().__getitem__(self, k)

	async def __aiter__(self):
		for item in super().items(self):
			yield item
