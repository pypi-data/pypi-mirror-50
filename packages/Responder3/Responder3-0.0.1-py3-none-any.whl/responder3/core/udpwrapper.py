import asyncio
import socket
import io
import ipaddress

from responder3.core.sockets import setup_base_socket


def recvfrom(loop, sock, n_bytes, fut=None, registed=False):
	fd = sock.fileno()
	if fut is None:
		fut = loop.create_future()
	if registed:
		loop.remove_reader(fd)

	try:
		data, addr = sock.recvfrom(n_bytes)
	except (BlockingIOError, InterruptedError):
		loop.add_reader(fd, recvfrom, loop, sock, n_bytes, fut, True)
	else:
		fut.set_result((data, addr))
	return fut


def sendto(loop, sock, data, addr, fut=None, registed=False):
	fd = sock.fileno()
	if fut is None:
		fut = loop.create_future()
	if registed:
		loop.remove_writer(fd)
	if not data:
		return

	try:
		n = sock.sendto(data, addr)	
	except (BlockingIOError, InterruptedError):
		loop.add_writer(fd, sendto, loop, sock, data, addr, fut, True)
	else:
		fut.set_result(n)
	return fut


class UDPReader:
	def __init__(self, data, addr):
		"""
		Lightweight wrapper around a UDP socket to provide the same interface as asyncio.StreamReader

		:param data: Data read from the socket
		:type data: bytearray
		:param addr: The socket address of the remote peer
		:type addr: tuple
		"""
		self._ldata = len(data)
		self._remaining = len(data)
		self._addr = addr
		self.buff = io.BytesIO(data)

	@asyncio.coroutine
	def read(self, n = -1):
		if n == -1:
			self._remaining = 0
		else:
			self._remaining -= n
		
		return self.buff.read(n)

	async def readline(self):
		data = self.buff.readline()
		self._remaining -= len(data)
		return data

	async def readuntil(self, separator=b'\n'):
		try:
			#ugly ugly ugly
			pos = self.buff.tell()
			temp = self.buff.read()
			m =  temp.find(separator)
			if m != -1:
				data = temp[:m]
				self.buff.seek(pos + m+1, 0)
				self._remaining -= len(data)
				return data
			
			else:
				self.buff.seek(pos, 0)
				raise Exception('Pattern not found!')
		except Exception as e:
			print(e)
		

	@asyncio.coroutine
	def readexactly(self, n):
		if n == -1:
			self._remaining = 0
		else:
			self._remaining -= n
		return self.buff.read(n)

	def at_eof(self):
		return self._remaining == 0


class UDPWriter:
	def __init__(self, loop, sock, addr, laddr):
		"""
		Lightweight wrapper around a UDP socket to provide the same interface as asyncio.StreamWriter
		:param loop: The main event loop
		:param sock: Socket used to read data from client
		:type sock: socket.socket
		:param addr: Address of the remote peer
		:type addr: tuple
		:param laddr: Address of the local side of the socket
		:type param: tuple
		"""
		self._laddr = laddr
		self._addr = addr
		self._loop = loop
		self._sock = sock

	# TODO: implement close function
	def close(self):
		return

	def get_extra_info(self, info, default=None):
		if info == 'socket':
			return self._sock
		elif info == 'peername':
			return self._addr
		elif info == 'sockname':
			return self._laddr
		else:
			return default

	def get_remote_address(self):
		return self._addr

	def get_local_address(self):
		return self._laddr

	@asyncio.coroutine
	def drain(self):
		return

	"""
	@asyncio.coroutine
	def write(self, data, addr = None):
		if addr is None:
			yield from sendto(self._loop, self._sock, data, self._addr)
		else:
			yield from sendto(self._loop, self._sock, data, addr)
	"""

	def write(self, data, addr = None):
		if addr is None:
			sendto(self._loop, self._sock, data, self._addr)
		else:
			sendto(self._loop, self._sock, data, addr)


class UDPClient:
	def __init__(self, raddr, loop = None, sock = None):
		"""
		Implements a client for asynchronous UDP communications.
		Don't fool yourself this is just a hackish solution to get asyncio streams-like functionality for UDP
		:param raddr: Address to connect to
		:type raddr: tuple
		:param loop: Main event loop
		:param sock: An already set-up socket to wrap
		:type sock: socket.socket
		"""
		self._raddr  = raddr
		self._socket = sock
		self._loop   = loop
		self._laddr  = None
		if loop is None:
			self._loop = asyncio.get_event_loop()

	def start_socket(self):
		family = socket.AF_INET if ipaddress.ip_address(self._raddr[0]).version == 4 else socket.AF_INET6
		self._socket = socket.socket(family, socket.SOCK_DGRAM, 0)
		self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self._socket.setblocking(False)
		self._socket.bind(('', 0))
		self._laddr  = self._socket.getsockname()

	async def run(self, data):
		"""
		Main function.
		:param data: data to send
		:type data: bytearray
		:return: UDPReader, UDPWriter
		"""
		if self._socket is None:
			self.start_socket()
		writer = UDPWriter(self._loop, self._socket, self._raddr, self._laddr)
		writer.write(data)
		data, addr = await recvfrom(self._loop, self._socket, 65536)
		reader = UDPReader(data, addr)
		return reader, writer


# https://www.pythonsheets.com/notes/python-asyncio.html
class UDPServer:
	def __init__(self, callback, listener_socket_config, loop = None, sock = None):
		"""

		:param callback: Function to handle new clients
		:type callback: fnc
		:param server_config: Server configuration
		:type server_config: ServerConfig
		:param loop: Main event loop
		:param sock: Already set-up socket object, if specified it will be used for comms
		:type sock: socket.socket
		"""
		self._callback = callback
		self.listener_socket_config = listener_socket_config
		self._socket = sock
		self._loop   = loop
		if self.listener_socket_config is None:
			if self._socket is None:
				raise Exception('Either socket or server_properties MUST be defined!')
			self._laddr  = self._socket.getsockname()
		else:
			self._laddr  = (str(self.listener_socket_config.bind_addr), self.listener_socket_config.bind_port)
		if loop is None:
			self._loop = asyncio.get_event_loop()

	async def serve_forever(self):
		if self._socket is None:
			self._socket = setup_base_socket(self.listener_socket_config)
		while True:
			data, addr = await recvfrom(self._loop, self._socket, 65536)
			reader = UDPReader(data, addr)
			writer = UDPWriter(self._loop, self._socket, addr, self._laddr)
			await self._callback(reader, writer)

	async def run(self):
		"""
		Main function. Create the reader and writer objects and calls the callback function.
		:return: None
		"""
		return await self.serve_forever()
