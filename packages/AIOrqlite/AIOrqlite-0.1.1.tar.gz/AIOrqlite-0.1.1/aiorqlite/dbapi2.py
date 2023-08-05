from __future__ import unicode_literals

import time
import asyncio
import functools

from .constants import (
    UNLIMITED_REDIRECTS,
)

from .connections import Connection
connect = Connection

from .exceptions import (
    Warning,
    Error,
    InterfaceError,
    DataError,
    DatabaseError,
    OperationalError,
    IntegrityError,
    InternalError,
    NotSupportedError,
    ProgrammingError,
)

from .types import (
    Binary,
    Date,
    Time,
    Timestamp,
    STRING,
    BINARY,
    NUMBER,
    DATETIME,
    ROWID,
)

# Compat with native sqlite module
from .extensions import converters, adapters, register_converter, register_adapter
from sqlite3.dbapi2 import PrepareProtocol

paramstyle = "qmark"

threadsafety = 1

apilevel = "2.0"

async def DateFromTicks(ticks):
    return Date(*time.localtime(ticks)[:3])

async def TimeFromTicks(ticks):
    return Time(*time.localtime(ticks)[3:6])

async def TimestampFromTicks(ticks):
    return Timestamp(*time.localtime(ticks)[:6])

def arun(func):
	@functools.wraps(func)
	def runner(*args, **kwargs):
		loop = asyncio.get_event_loop()
		result = loop.run_until_complete(func(*args, **kwargs))
		return result
	return runner

# accessed by sqlalchemy sqlite dialect
sqlite_version_info = (3, 10, 0)

# Compat with native sqlite module
from .extensions import PARSE_DECLTYPES, PARSE_COLNAMES
