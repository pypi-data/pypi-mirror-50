import logging
import asyncio
import email.parser

from responder3.core.logging.logger import *
from responder3.core.asyncio_helpers import R3ConnectionClosed
from responder3.core.commons import *
from responder3.protocols.SMTP import *
from responder3.core.servertemplate import ResponderServer, ResponderServerSession
from responder3.core.ssl import get_default_server_ctx


class SMTPSession(ResponderServerSession):
	def __init__(self, connection, log_queue):
		ResponderServerSession.__init__(self, connection, log_queue, self.__class__.__name__)
		self.creds = {} # {'alma':'alma2'}
		self.salt = None
		self.encoding = 'utf8'  # THIS CAN CHANGE ACCORING TO CLIENT REQUEST!!!
		self.parser = SMTPCommandParser(encoding=self.encoding)
		self.emailparser = email.parser.Parser()
		self.current_state = SMTPServerState.START
		self.supported_auth_types = [SMTPAuthMethod.LOGIN, SMTPAuthMethod.PLAIN, SMTPAuthMethod.CRAM_MD5]
		self.authhandler = None
		self.emailFrom = ''
		self.emailTo = []
		self.ssl_ctx = None

		self.capabilities = []
		self.helo_msg = None
		self.ehlo_msg = None
		#self.log_data = False


	def __repr__(self):
		t = '== SMTP Session ==\r\n'
		t += 'encoding     : %s\r\n' % repr(self.encoding)
		t += 'parser       : %s\r\n' % repr(self.parser)
		t += 'current_state: %s\r\n' % repr(self.current_state)
		t += 'authhandler  : %s\r\n' % repr(self.authhandler)
		return t


class SMTP(ResponderServer):
	def init(self):
		if self.settings:
			self.parse_settings()
			return
		self.set_default_settings()

	def set_default_settings(self):
		self.session.salt = '<1896.697170952@dbc.mtview.ca.us>' #this salt is used for CRAM-MD5
		self.session.helo_msg = 'mx.bocisajt.com Microsoft ESMTP MAIL Service ready'
		self.session.ehlo_msg = 'mx.bocisajt.com Microsoft ESMTP MAIL Service ready'
		self.session.capabilities.append('SMTPUTF8')
		self.session.capabilities.append('STARTTLS')
		if self.session.supported_auth_types is not None:
			self.session.capabilities.append('AUTH ' + ' '.join([a.name for a in self.session.supported_auth_types]))

		self.session.ssl_ctx = get_default_server_ctx()

	def parse_settings(self):
		if 'helo_msg' in self.settings:
			self.session.helo_msg = self.settings['helo_msg']
			self.session.ehlo_msg = self.settings['helo_msg']
		if 'ehlo_msg' in self.settings:
			self.session.ehlo_msg = self.settings['ehlo_msg']
			if not self.session.helo_msg:
				elf.session.helo_msg = self.settings['ehlo_msg']
		if 'salt' in self.settings:
			self.session.salt = self.settings['salt']
		# TODO: set atuth types from config!
		# then comment out the following lines
		if self.session.supported_auth_types is not None:
			self.session.capabilities.append('AUTH ' + ' '.join([a.name for a in self.session.supported_auth_types]))
		

	async def send_data(self, data):
		self.cwriter.write(data)
		await self.cwriter.drain()

	@r3trafficlogexception
	async def run(self):
		# send hello
		await asyncio.wait_for(
			self.send_data(SMTPReply.construct(220, '%s %s' % (self.session.helo_msg, self.session.salt)).to_bytes()), timeout=1)

		# main loop
		while not self.shutdown_evt.is_set():
			try:
				result = await asyncio.gather(*[asyncio.wait_for(self.session.parser.from_streamreader(self.creader), timeout=None)], return_exceptions=True)
			except asyncio.CancelledError as e:
				raise e
			if isinstance(result[0], R3ConnectionClosed):
				return
			elif isinstance(result[0], Exception):
				raise result[0]
			else:
				cmd = result[0]

			print(cmd)
			if 'R3DEEPDEBUG' in os.environ:
				await self.logger.debug(cmd)
				await self.logger.debug(self.session.current_state)

			if cmd.command == SMTPCommand.QUIT:
				await asyncio.wait_for(
						self.send_data(SMTPReply.construct(221).to_bytes()),
						timeout=1)
				return

			if self.session.current_state == SMTPServerState.START:
				if cmd.command == SMTPEHLOCmd or cmd.command == SMTPHELOCmd:
					if self.session.supported_auth_types is None:
						self.session.current_state = SMTPServerState.AUTHENTICATED

				if cmd.command == SMTPCommand.HELO:
					await asyncio.wait_for(
						self.send_data(
							SMTPReply.construct(250, [self.session.helo_msg] + self.session.capabilities).to_bytes()),
						timeout=1)
					continue

				elif cmd.command == SMTPCommand.EHLO:
					await asyncio.wait_for(
						self.send_data(
							SMTPReply.construct(250, [self.session.ehlo_msg] + self.session.capabilities).to_bytes()),
						timeout=1)
					continue

				elif cmd.command == SMTPCommand.STARTTLS:
					self.cwriter.pause_reading()
					await asyncio.wait_for(
						self.send_data(
							SMTPReply.construct(220, 'Go ahead').to_bytes()),
						timeout=1)
					await self.switch_ssl(self.session.ssl_ctx)
					continue

				elif cmd.command == SMTPCommand.EXPN:
					await asyncio.wait_for(
						self.send_data(SMTPReply.construct(502).to_bytes()),
						timeout=1)
					continue

				elif cmd.command == SMTPCommand.VRFY:
					await asyncio.wait_for(
						self.send_data(SMTPReply.construct(502).to_bytes()),
						timeout=1)
					continue

				elif cmd.command == SMTPCommand.AUTH:
					self.session.current_state = SMTPServerState.AUTHSTARTED
					# NOTE: the protocol allows the authentication data to be sent immediately by the client
					# if this happens, the initdata will be not none and needs to be evaluated.
					if cmd.mechanism == 'PLAIN':
						self.session.authhandler = SMTPAuthHandler(SMTPAuthMethod.PLAIN, self.session.creds)
						if cmd.data is not None:
							res, cred = self.session.authhandler.do_AUTH(cmd)
							if cred is not None:
								await self.logger.credential(cred)
							if res == SMTPAuthStatus.OK:
								self.session.current_state = SMTPServerState.AUTHENTICATED
								await asyncio.wait_for(
									self.send_data(SMTPReply.construct(235).to_bytes()),
									timeout=1)
								continue
							else:
								await asyncio.wait_for(
									self.send_data(SMTPReply.construct(535).to_bytes()),
									timeout=1)
								return
						else:
							await asyncio.wait_for(
								self.send_data(SMTPReply.construct(334).to_bytes()),
								timeout=1)
							continue

					elif cmd.mechanism == 'LOGIN':
						self.session.authhandler = SMTPAuthHandler(SMTPAuthMethod.LOGIN, self.session.creds)
						await asyncio.wait_for(
								self.send_data(SMTPReply.construct(334, 'VXNlcm5hbWU6').to_bytes()),
								timeout=1)
						continue
					else:
						await asyncio.wait_for(
							self.send_data(SMTPReply.construct(535).to_bytes()),
							timeout=1)
						raise Exception('Not supported auth mechanism, client tried to use %s' % cmd.mechanism)
				else:
					await asyncio.wait_for(
						self.send_data(SMTPReply.construct(503).to_bytes()),
						timeout=1)
					continue

			# this state is only for the authentication part
			elif self.session.current_state == SMTPServerState.AUTHSTARTED:
				"""
				here we expect to have non-smtp conform messages (without command code)
				"""
				if cmd.command == SMTPCommand.XXXX:
					res, res_data = self.session.authhandler.do_AUTH(cmd)
					if res in [SMTPAuthStatus.OK, SMTPAuthStatus.NO]:
						if res_data is not None:
							await self.logger.credential(res_data)
							
					if res == SMTPAuthStatus.OK:
						self.session.current_state = SMTPServerState.AUTHENTICATED
						await asyncio.wait_for(
							self.send_data(SMTPReply.construct(235).to_bytes()),
							timeout=1)
						continue

					if res == SMTPAuthStatus.MORE_DATA_NEEDED:
						await asyncio.wait_for(
						self.send_data(SMTPReply.construct(334, res_data).to_bytes()),
							timeout=1)
						continue
						
					if res == SMTPAuthStatus.NO:
						await asyncio.wait_for(
							self.send_data(SMTPReply.construct(535).to_bytes()),
							timeout=1)
						return

			# should be checking which commands are allowed in this state...
			elif self.session.current_state == SMTPServerState.AUTHENTICATED:
				if cmd.command == SMTPCommand.MAIL:
					self.session.emailFrom = cmd.emailaddress
					await asyncio.wait_for(
						self.send_data(SMTPReply.construct(250).to_bytes()),
						timeout=1)
					continue

				elif cmd.command == SMTPCommand.RCPT:
					self.session.emailTo.append(cmd.emailaddress)
					await asyncio.wait_for(
						self.send_data(SMTPReply.construct(250).to_bytes()),
						timeout=1)
					continue

				elif cmd.command == SMTPCommand.DATA:
					# we get data command, switching current_state and sending a reply to client can send data
					if cmd.emaildata is None:
						await asyncio.wait_for(
							self.send_data(SMTPReply.construct(354).to_bytes()),
							timeout=1)
						continue
					else:
						em = EmailEntry()
						em.email = self.session.emailparser.parsestr(cmd.emaildata)
						em.fromAddress = self.session.emailFrom  # string
						em.toAddress = self.session.emailTo  # list
						await self.logger.email(em)
						await asyncio.wait_for(
							self.send_data(SMTPReply.construct(250).to_bytes()),
							timeout=1)
						continue
				else:
					await asyncio.wait_for(
						self.send_data(SMTPReply.construct(503).to_bytes()),
						timeout=1)
					return

			else:
				await asyncio.wait_for(
					self.send_data(SMTPReply.construct(503).to_bytes()),
					timeout=1)
				return
