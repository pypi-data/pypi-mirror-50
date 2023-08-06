from __future__ import unicode_literals

import json
import logging
import sys
import re

try:
	# pylint: disable=no-name-in-module
	from urllib.parse import urlencode
except ImportError:
	# pylint: disable=no-name-in-module
	from urllib import urlencode

from .exceptions import Error, ProgrammingError

from .row import Row
from .extensions import _convert_to_python, _adapt_from_python, _column_stripper

if sys.version_info[0] >= 3:
	basestring = str
	_urlencode = urlencode
else:
	# avoid UnicodeEncodeError from urlencode
	def _urlencode(query, doseq=0):
		return urlencode(dict(
			(k if isinstance(k, bytes) else k.encode('utf-8'),
			 v if isinstance(v, bytes) else v.encode('utf-8'))
			for k, v in query.items()), doseq=doseq)

class Cursor(object):
	arraysize = 1

	def __init__(self, connection):
		self._connection = connection
		self.messages = []
		self.lastrowid = None
		self.description = None
		self.rownumber = 0
		self.rowcount = -1
		self.arraysize = 1
		self._rows = None
		self._column_type_cache = {}

	async def __aenter__(self):
		return self

	async def __aexit__(self, exc_type, exc_value, exc_traceback):
		await self.close()

	@property
	def connection(self):
		return self._connection

	async def close(self):
		self._rows = None

	async def _request(self, method, uri, body=None, headers={}):
		logger = logging.getLogger(__name__)
		debug = logger.getEffectiveLevel() < logging.DEBUG
		logger.debug(
			'request method: %s uri: %s headers: %s body: %s',
			method,
			uri,
			headers,
			body)
		response = await self.connection._fetch_response(
			method, uri, body=body, headers=headers)
		logger.debug(
			"status: %s reason: %s",
			response.status,
			response.reason)
		response_text = await response.read()
		response_text = response_text.decode('utf-8')
		logger.debug("raw response: %s", response_text)
		response_json = json.loads(
			response_text, object_pairs_hook=dict)
		if debug:
			logger.debug(
				"formatted response: %s",
				json.dumps(
					response_json,
					indent=4))
		return response_json

	async def _substitute_params(self, operation, parameters):
		'''
		SQLite natively supports only the types TEXT, INTEGER, REAL, BLOB and
		NULL
		'''

		param_matches = 0

		qmark_re = re.compile(r"(\?)")
		named_re = re.compile(r"(:{1}[a-zA-Z]+?\b)")

		qmark_matches = qmark_re.findall(operation)
		named_matches = named_re.findall(operation)
		param_matches = len(qmark_matches) + len(named_matches)

		# Matches but no parameters
		if param_matches > 0 and parameters is None:
			raise ProgrammingError('paramater required but not given: %s' %
								   operation)

		# No regex matches and no parameters.
		if parameters is None:
			return operation

		if len(qmark_matches) > 0 and len(named_matches) > 0:
			raise ProgrammingError('different paramater types in operation not'
								   'permitted: %s %s' % 
								   (operation, parameters))

		if isinstance(parameters, dict):
			# parameters is a dict or a dict subclass
			if len(qmark_matches) > 0:
				raise ProgrammingError('Unamed binding used, but you supplied '
									   'a dictionary (which has only names): '
									   '%s %s' % (operation, parameters))
			for op_key in named_matches:
				try:
					operation = operation.replace(op_key, 
												 _adapt_from_python(parameters[op_key[1:]]))
				except KeyError:
					raise ProgrammingError('the named parameters given do not '
										   'match operation: %s %s' %
										   (operation, parameters))
		else:
			# parameters is a sequence
			if param_matches != len(parameters):
				raise ProgrammingError('incorrect number of parameters '
									   '(%s != %s): %s %s' % (param_matches, 
									   len(parameters), operation, parameters))
			if len(named_matches) > 0:
				raise ProgrammingError('Named binding used, but you supplied a'
									   ' sequence (which has no names): %s %s' %
									   (operation, parameters))
			for i in range(len(parameters)):
				operation = operation.replace('?', 
											  _adapt_from_python(parameters[i]), 1)

		return operation

	async def _get_sql_command(self, sql_str):
		return sql_str.split(None, 1)[0].upper()

	async def execute(self, operation, parameters=None):
		if not isinstance(operation, basestring):
			raise ValueError(
							 "argument must be a string, not '{}'".format(type(operation).__name__))

		operation = await self._substitute_params(operation, parameters)

		command = await self._get_sql_command(operation)
		if command in ('SELECT', 'PRAGMA'):
			payload = await self._request("GET",
									"/db/query?" + _urlencode({'q': operation}))
		else:
			payload = await self._request("POST", "/db/execute?transaction",
									headers={'Content-Type': 'application/json'}, body=json.dumps([operation]))

		last_insert_id = None
		rows_affected = -1
		payload_rows = {}
		try:
			results = payload["results"]
		except KeyError:
			pass
		else:
			rows_affected = 0
			for item in results:
				if 'error' in item:
					logging.getLogger(__name__).error(json.dumps(item))
					raise Error(json.dumps(item))
				try:
					rows_affected += item['rows_affected']
				except KeyError:
					pass
				try:
					last_insert_id = item['last_insert_id']
				except KeyError:
					pass
				if 'columns' in item:
					payload_rows = item

		try:
			fields = payload_rows['columns']
		except KeyError:
			self.description = None
			self._rows = []
			if command == 'INSERT':
				self.lastrowid = last_insert_id
		else:
			rows = []
			description = []
			for field in fields:
				description.append((
					_column_stripper(field, parse_colnames=self.connection.parse_colnames),
					None,
					None,
					None,
					None,
					None,
					None,
				))

			try:
				values = payload_rows['values']
				types = payload_rows['types']
			except KeyError:
				pass
			else:
				if values:
					converters = [_convert_to_python(field, type_,
								  parse_decltypes=self.connection.parse_decltypes,
								  parse_colnames=self.connection.parse_colnames)
								  for field, type_ in zip(fields, types)]
					for payload_row in values:
						row = []
						for field, converter, value in zip(fields, converters, payload_row):
							row.append((field, (value if converter is None
												else converter(value))))
						rows.append(Row(row))
			self._rows = rows
			self.description = tuple(description)

		self.rownumber = 0
		if command in ('UPDATE', 'DELETE'):
			# sqalchemy's _emit_update_statements function asserts
			# rowcount for each update, and _emit_delete_statements
			# warns unless rowcount matches
			self.rowcount = rows_affected
		else:
			self.rowcount = len(self._rows)
		return self

	async def executemany(self, operation, seq_of_parameters=None):
		if not isinstance(operation, basestring):
			raise ValueError(
				"argument must be a string, not '{}'".format(type(operation).__name__))

		statements = []
		for parameters in seq_of_parameters:
			statements.append(await self._substitute_params(operation, parameters))
		payload = await self._request("POST", "/db/execute?transaction",
								headers={'Content-Type': 'application/json'},
								body=json.dumps(statements))
		rows_affected = -1
		try:
			results = payload["results"]
		except KeyError:
			pass
		else:
			rows_affected = 0
			for item in results:
				if 'error' in item:
					logging.getLogger(__name__).error(json.dumps(item))
				try:
					rows_affected += item['rows_affected']
				except KeyError:
					pass
		self._rows = []
		self.rownumber = 0
		self.rowcount = rows_affected

	async def fetchone(self):
		''' Fetch the next row '''
		if self._rows is None or self.rownumber >= len(self._rows):
			return None
		result = self._rows[self.rownumber]
		self.rownumber += 1
		return result

	async def fetchmany(self, size=None):
		remaining = self.arraysize if size is None else size
		remaining = min(remaining, self.rowcount - self.rownumber)
		return [self.fetchone() for i in range(remaining)]

	async def fetchall(self):
		rows = []
		while self.rownumber < self.rowcount:
			row = await self.fetchone()
			rows.append(row)
		return rows

	async def setinputsizes(self, sizes):
		raise NotImplementedError(self)

	async def setoutputsize(self, size, column=None):
		raise NotImplementedError(self)

	async def scroll(self, value, mode='relative'):
		raise NotImplementedError(self)

	async def next(self):
		raise NotImplementedError(self)

	async def __aiter__(self):
		while self.rownumber < self.rowcount:
			row = await self.fetchone()
			yield row
