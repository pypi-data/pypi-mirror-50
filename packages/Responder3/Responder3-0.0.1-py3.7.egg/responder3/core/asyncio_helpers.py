import asyncio


async def generic_read(reader, n):
	return reader.read(n)


async def generic_write(writer, data):
	writer.write(data)
	await writer.drain()


async def readexactly_or_exc(reader, n, timeout = None):
	"""
	Helper function to read exactly N amount of data from the wire.
	:param reader: The reader object
	:type reader: asyncio.StreamReader
	:param n: The maximum amount of bytes to read.
	:type n: int
	:param timeout: Time in seconds to wait for the reader to return data
	:type timeout: int
	:return: bytearray
	"""
	temp = await asyncio.gather(*[asyncio.wait_for(reader.readexactly(n), timeout = timeout)], return_exceptions=True)
	if isinstance(temp[0], bytes):
		return temp[0]
	else:
		raise temp[0]

	return data


async def read_or_exc(reader, n, timeout = None):
	"""
	Helper function to read N amount of data from the wire.
	:param reader: The reader object
	:type reader: asyncio.StreamReader
	:param n: The maximum amount of bytes to read. BEWARE: this only sets an upper limit of the data to be read
	:type n: int
	:param timeout: Time in seconds to wait for the reader to return data
	:type timeout: int
	:return: bytearray
	"""

	temp = await asyncio.gather(*[asyncio.wait_for(reader.read(n), timeout = timeout)], return_exceptions=True)
	if isinstance(temp[0], bytes):
		return temp[0]
	else:
		raise temp[0]

	return data


async def readuntil_or_exc(reader, pattern, timeout = None):
	"""
	Helper function to read the wire until a certain pattern is reached.
	:param reader: The reader object
	:type reader: asyncio.StreamReader
	:param pattern: The pattern marking the end of read
	:type pattern: bytearray
	:param timeout: Time in seconds to wait for the reader to reach the pattern
	:type timeout: int
	:return: bytearray
	"""

	temp = await asyncio.gather(*[asyncio.wait_for(reader.readuntil(pattern), timeout = timeout)], return_exceptions=True)
	if isinstance(temp[0], bytes):
		return temp[0]
	else:
		raise temp[0]



async def readline_or_exc(reader, timeout = None):
	"""
	Helper function to read the wire until an end-of-line character is reached.
	:param reader: The reader object
	:type reader: asyncio.StreamReader
	:param timeout: Time in seconds to wait for the reader to reach the pattern
	:type timeout: int
	:return: bytearray
	"""

	temp = await asyncio.gather(*[asyncio.wait_for(reader.readline(), timeout = timeout)], return_exceptions=True)
	if isinstance(temp[0], bytes):
		return temp[0]
	else:
		raise temp[0]


async def sendall(writer, data):
	"""
	Helper function that writes all the data to the wire
	:param writer: Writer object
	:type writer: asyncio.StreamWriter
	:param data: Data to be written
	:type data: bytearray
	:return: None
	"""
	try:
		writer.write(data)
		await writer.drain()
	except Exception as e:
		raise R3ConnectionClosed()


class R3ConnectionClosed(Exception):
	pass


@asyncio.coroutine
async def wait_mp_event(event, aio_event):
	event.wait(timeout = None)
	aio_event.set()
	return
