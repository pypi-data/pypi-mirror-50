from __future__ import unicode_literals

import codecs
import logging
import aiohttp
import asyncio

try:
	from urllib.parse import urlparse
except ImportError:
	# pylint: disable=import-error
	from urlparse import urlparse

from .constants import (
	UNLIMITED_REDIRECTS,
)

from .cursors import Cursor
from ._ephemeral import EphemeralRqlited as _EphemeralRqlited
from .extensions import PARSE_DECLTYPES, PARSE_COLNAMES

class Connection(object):
	from .exceptions import (
		Warning,
		Error,
		InterfaceError,
		DatabaseError,
		DataError,
		OperationalError,
		IntegrityError,
		InternalError,
		ProgrammingError,
		NotSupportedError,
	)

	def __init__(self, host='localhost', port=None,
				 user=None, password=None, connect_timeout=None,
				 detect_types=0, max_redirects=UNLIMITED_REDIRECTS):

		self.messages = []
		self.host = host
		self.port = port
		if not self.port:
			if self.host.count(':') == 1:
				split = self.host.split(':')
				self.host = split[0]
				self.port = int(split[1])
		if not self.port:
			self.port = 4001
		self._headers = {}
		if not (user is None or password is None):
			self._headers['Authorization'] = 'Basic ' + \
				codecs.encode('{}:{}'.format(user, password).encode('utf-8'),
							  'base64').decode('utf-8').rstrip('\n')

		self.connect_timeout = connect_timeout
		self.max_redirects = max_redirects
		self.detect_types = detect_types
		self.parse_decltypes = detect_types & PARSE_DECLTYPES
		self.parse_colnames = detect_types & PARSE_COLNAMES
		self._ephemeral = None
		if self.host == ':memory:':
			self._ephemeral = _EphemeralRqlited()

		self._enter = False

	async def __aenter__(self):
		if not self._enter:
			self._connection = await self._init_connection()
			if self._ephemeral:
				self._ephemeral = await self._ephemeral.__aenter__()
				self.host, self.port = self._ephemeral.http
		self._enter = True
		return self

	async def __aexit__(self, exc_type, exc, tb):
		self._enter = False
		await self.close()

	async def _init_connection(self):
		timeout = aiohttp.ClientTimeout(total=None, connect=None, sock_connect=None, sock_read=None)
		if self.connect_timeout:
			timeout.total = float(self.connect_timeout)
		return aiohttp.ClientSession(timeout=timeout)

	async def _retry_request(self, method, uri, body=None, headers={}):
		tries = 10
		while tries:
			tries -= 1
			try:
				resp = await self._connection.request(method, 'http://%s:%s%s' % (self.host, self.port, uri), data=body,
										 headers=dict(self._headers, **headers))
				return resp
			except Exception:
				if not tries:
					raise
				if self._ephemeral:
					await asyncio.sleep(0.5) # allow delay for server to start
				await self._connection.close()
				self._connection = await self._init_connection()

	async def _fetch_response(self, method, uri, body=None, headers={}):
		"""
		Fetch a response, handling redirection.
		"""
		response = await self._retry_request(method, uri, body=body, headers=headers)
		redirects = 0

		while response.status == 301 and \
				response.headers.get('Location') is not None and \
				(self.max_redirects == UNLIMITED_REDIRECTS or redirects < self.max_redirects):
			redirects += 1
			uri = response.headers.get('Location')
			location = urlparse(uri)

			logging.getLogger(__name__).debug("status: %s reason: '%s' location: '%s'",
											  response.status, response.reason, uri)

			if self.host != location.hostname or self.port != location.port:
				await self._connection.close()
				self.host = location.hostname
				self.port = location.port
				self._connection = await self._init_connection()

			response = await self._retry_request(method, uri, body=body, headers=headers)

		return response

	async def close(self):
		"""Close the connection now (rather than whenever .__del__() is
		called).

		The connection will be unusable from this point forward; an
		Error (or subclass) exception will be raised if any operation
		is attempted with the connection. The same applies to all
		cursor objects trying to use the connection. Note that closing
		a connection without committing the changes first will cause an
		implicit rollback to be performed."""
		await self._connection.close()
		if self._ephemeral is not None:
			await self._ephemeral.__aexit__(None, None, None)
			self._ephemeral = None

	def __del__(self):
		""" cannot asynchronously delete """
		pass

	async def commit(self):
		"""Database modules that do not support transactions should
		implement this method with void functionality."""
		pass

	async def rollback(self):
		"""This method is optional since not all databases provide
		transaction support. """
		pass

	def cursor(self, factory=Cursor):
		"""Return a new Cursor Object using the connection."""
		return factory(self)

	async def execute(self, *args, **kwargs):
		curs = self.cursor()
		c = await curs.__aenter__()
		await c.execute(*args, **kwargs)
		return curs
