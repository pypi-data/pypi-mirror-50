import os
import sys
import copy
import json
import logging
import argparse
import datetime
import asyncio
import itertools
import importlib.machinery
import importlib.util
import warnings

from responder3.core.commons import handle_systemd, defaultports, tracefunc
from responder3.core.interfaces.NetworkInterfaces import interfaces
from responder3.core.logging.logger import *
from responder3.core.logging.logtask import *
from responder3.core.servertask import Responder3ServerTask
from responder3.core.rdns import RDNS
from responder3.core.manager.r3manager_client import *
from responder3.core.manager.r3manager_server import *


class ServerTaskEntry:
	def __init__(self, taskid):
		self.taskid = taskid
		self.startup_config = None
		self.task = None
		self.server = None
		self.command_channel_manager = asyncio.Queue()
		self.command_channel_client = asyncio.Queue()
		#self.shutdown_event = asyncio.Event()
		self.created_at = datetime.datetime.utcnow()
		self.started_at = None


class Responder3:
	def __init__(self):
		self.loop = asyncio.get_event_loop()
		self.config = None

		self.reverse_domain_table = {}
		self.resolver_server = [{'ip':'8.8.8.8', 'port':53, 'proto' : 'udp'}]
		self.resolver_server6 = [{ 'ip': '2001:4860:4860::8888', 'port':53, 'proto' : 'udp'}]


		self.log_queue = asyncio.Queue()
		self.logger = Logger('Responder3 MAIN', logQ = self.log_queue)
		self.log_command_queue = asyncio.Queue()
		self.logprocessor = None
		self.test_output_queue = None #log queue for tests only
		self.manager_log_queue = None #this wueue is to dispatch all local log objects to the manager object if any

		self.override_interfaces = None
		self.override_ipv4 = None
		self.override_ipv6 = None
		self.override_verb = None

		self.server_task_id = 0
		self.servers = []
		self.server_tasks = {}
		
		self.manager_task = None
		self.manager_cmd_queue_in = asyncio.Queue()
		self.manager_cmd_queue_out = asyncio.Queue()
		self.manager_shutdown_evt = asyncio.Event()

		self.shutdown_evt = asyncio.Event()


	@staticmethod
	def get_argparser():
		parser = argparse.ArgumentParser(
			description='Responder3',
			epilog='List of available interfaces:\r\n' + str(interfaces),
			formatter_class=argparse.RawTextHelpFormatter
		)
		parser.add_argument(
			"-c",
			"--config",
			help="Configuration file (JSON). Full path please"
		)
		parser.add_argument(
			"-p",
			"--python-config",
			help="Configuration file (Python). Full path please"
		)
		parser.add_argument(
			"-e",
			"--environ-config",
			action='store_true',
			help="Configuration file is set via OS environment variable (Python script)"
		)
		parser.add_argument(
			"-I",
			action='append',
			help="Interface to bind to, can be multiple by providing sequential -I. Overrides bind_iface parameter in configs."
		)
		parser.add_argument(
			"-4",
			action='store_true',
			dest='ip4',
			help="IP version 4 to be used. Overrides bind_family in config settings."
		)
		parser.add_argument(
			"-6",
			action='store_true',
			dest='ip6',
			help="IP version 6 to be used. Overrides bind_family in config settings."
		)
		parser.add_argument(
			"-L",
			action='store_true',
			dest='list_interfaces',
			help="List all interfaces with assigned IPv4 and IPv6 addresses then exit."
		)
		parser.add_argument(
			'-v',
			'--verbose',
			action='count',
			default=0
		)
		return parser

	@staticmethod
	def from_args(args):
		if args.list_interfaces == True:
			print('====== Interfaces list ======')
			print(interfaces)
			return None

		responder = Responder3()
		responder.override_interfaces = args.I
		responder.override_ipv4 = args.ip4
		responder.override_ipv6 = args.ip6
		responder.override_verb = args.verbose
		if args.config is not None:
			responder.config = Responder3Config.from_file(args.config)
		elif args.python_config is not None:
			responder.config = Responder3Config.from_python_script(args.python_config)
		elif args.environ_config is not None:
			responder.config = Responder3Config.from_os_env()
		else:
			raise Exception(
				'No suitable configuration method was supplied!'
				'Use either -e or -c or -p'
			)
		return responder

	@staticmethod
	def from_config(config, override_interfaces = None, override_ipv4 = None, override_ipv6=None, override_verb=None, output_queue = None):
		responder = Responder3()
		responder.override_interfaces = override_interfaces
		responder.override_ipv4 = override_ipv4
		responder.override_ipv6 = override_ipv6
		responder.override_verb = override_verb
		responder.test_output_queue = output_queue
		responder.config = config
		return responder

	def get_taskid(self):
		taskid = self.server_task_id
		self.server_task_id += 1
		return taskid

	@r3exception
	async def start_server_task(self, serverconfig):
		ste = ServerTaskEntry(self.get_taskid())
		temp = copy.deepcopy(serverconfig)
		resolver_server = temp['resolver'] if 'resolver' in temp else self.resolver_server
		resolver_server6 = temp['resolver6'] if 'resolver6' in temp else self.resolver_server6
		ste.startup_config = temp
		ste.task = Responder3ServerTask(
			log_queue = self.log_queue,
			rdns_resolver = RDNS(resolver_server, resolver_server6),
			reverse_domain_table=self.reverse_domain_table,
			server_command_queue=None,
			loop=self.loop
		)
		ste.server = await ste.task.create_server(temp)
		self.server_tasks[ste.taskid] = ste
		asyncio.ensure_future(ste.server.serve_forever())
		ste.started_at = datetime.datetime.utcnow()
		del temp

		return ste.taskid

	@r3exception
	async def list_servers(self, cmd):
		print('list_servers')
		servers = {}
		for taskid in self.server_tasks:
			servers[taskid] = self.server_tasks[taskid].startup_config
		rply = R3CliListServersRply(servers = servers)
		await self.manager_cmd_queue_out.put(rply)


	@r3exception
	async def create_server(self, cmd):
		print('create_server')
		server_id = await self.start_server_task(cmd.server_config) #TODO! dict_config

		rply = R3CliCreateServerRply(server_id = server_id)
		await self.manager_cmd_queue_out.put(rply)
		
	@r3exception
	async def list_interfaces(self, cmd):
		try:
			print('list interfaces cmd in')
			ifs = {}
			
			for ifname in interfaces.interfaces:
				ifs[ifname] = interfaces.interfaces[ifname].to_json()
				
			rply = R3CliListInterfacesRply(interfaces = ifs)
			await self.manager_cmd_queue_out.put(rply)
			print('Reply sent')
		except Exception as e:
			traceback.print_exc()

	@r3exception
	async def stop_server(self, cmd):
		if cmd.server_id not in self.server_tasks:
			print('Server ID doesnt exist!')
			return
		
		try:
			self.server_tasks[cmd.server_id].server.close()
			del self.server_tasks[cmd.server_id]
			print(type(self.server_tasks[cmd.server_id].task))
		except Exception as e:
			traceback.print_exc()
			rply = R3CliServerStopRply(status = 'NO')
		else:
			rply = R3CliServerStopRply(status = 'OK')
		
		await self.manager_cmd_queue_out.put(rply)


	@r3exception
	async def shutdown(self, cmd):
		#TODO: make it fancy

		self.shutdown_evt.set()
		

	@r3exception
	async def handle_remote_commands(self):
		"""
		If manager is set up and is in CLIENT mode, 
		this method will handle the remote commands 
		coming from the remote manager server
		"""
		try:
			while True:
				cmd = await self.manager_cmd_queue_in.get()
				print(cmd.cmd_id)
				if cmd.cmd_id == R3ClientCommand.SHUTDOWN:
					await self.shutdown(cmd)
				elif cmd.cmd_id == R3ClientCommand.STOP_SERVER:
					await self.stop_server(cmd)
				elif cmd.cmd_id == R3ClientCommand.LIST_SERVERS:
					await self.list_servers(cmd)
				elif cmd.cmd_id == R3ClientCommand.CREATE_SERVER:
					await self.create_server(cmd)
				elif cmd.cmd_id == R3ClientCommand.LIST_INTERFACES:
					await self.list_interfaces(cmd)
				else:
					print('Unknown command in queue!')				
				
		except Exception as e:
			"""
			if there is an exception we set the shutdown event on the server
			"""
			traceback.print_exc()
			self.manager_shutdown_evt.set()
			return
		
	@r3exception
	async def start_manager(self):
		"""
		Start remote manager client/server if config has it
		"""
		if not self.config.manager_settings:
			return
		
		if self.config.manager_settings['mode'] == 'CLIENT':
			print('Starting manager in CLIENT mode')
			server_url = self.config.manager_settings['server_url']
			config = self.config.manager_settings['config']
			ssl_ctx = None
			if 'ssl_ctx' in self.config.manager_settings:
				ssl_ctx = self.config.manager_settings['ssl_ctx']
			
			asyncio.ensure_future(self.handle_remote_commands()) #starting command handler
			
			self.manager_task = Responder3ManagerClient(
								server_url, 
								config, 
								self.log_queue,
								self.manager_log_queue, 
								self.manager_cmd_queue_in, 
								self.manager_cmd_queue_out, 
								self.manager_shutdown_evt, 
								ssl_ctx
			)
			asyncio.ensure_future(self.manager_task.run())
		
		elif self.config.manager_settings['mode'] == 'SERVER':
			self.manager_log_queue = None #this queue is to dispatch all local log objects to the manager object if any
			self.manager_task = None
			
			print('Starting manager in SERVER mode')
			listen_ip = self.config.manager_settings['listen_ip']
			listen_port = self.config.manager_settings['listen_port']
			config = self.config.manager_settings['config']
			ssl_ctx = None
			if 'ssl_ctx' in self.config.manager_settings:
				ssl_ctx = self.config.manager_settings['ssl_ctx']
			
			
			self.manager_task = Responder3ManagerServer(listen_ip, listen_port, config, self.log_queue, self.log_queue, self.manager_cmd_queue_in, self.manager_cmd_queue_out, self.manager_shutdown_evt, ssl_ctx = ssl_ctx)
			asyncio.ensure_future(self.manager_task.run())
			
		
		else:
			raise Exception('Failed to set up manager! Unknown mode!')

	def get_serverconfigs(self):
		# Setting up and starting servers
		for serverentry in self.config.server_settings:
			if self.override_interfaces is None:
				ifaces = serverentry.get('bind_iface', None)
				if ifaces is None:
					raise Exception('Interface name MUST be provided!')
				if not isinstance(ifaces, list):
					ifaces = [ifaces]

			else:
				ifaces = self.override_interfaces
			bind_family = []
			if self.override_ipv4:
				bind_family.append(4)
			if self.override_ipv6:
				bind_family.append(6)

			if bind_family == []:
				bind_family_conf = serverentry.get('bind_family', None)
				if bind_family_conf is not None:
					if not isinstance(bind_family_conf, list):
						bind_family.append(int(bind_family_conf))
					else:
						for ver in bind_family_conf:
							bind_family.append(int(ver))

			if bind_family == []:
				raise Exception('IP version (bind_family) MUST be set either in config file or in command line!')

			portspecs = serverentry.get(
				'bind_port',
				defaultports[serverentry['handler']] if serverentry['handler'] in defaultports else None
			)

			if portspecs is None:
				raise Exception('For protocol %s the port must be supplied!' % (serverentry['handler'],))

			if not isinstance(portspecs, list):
				portspecs = [portspecs]

			for element in itertools.product(ifaces, portspecs):
				socket_configs = interfaces.get_socketconfig(
					element[0], element[1][0], element[1][1],
					ipversion=bind_family
				)
				for socket_config in socket_configs:
					serverentry['listener_socket_config'] = socket_config
					yield serverentry

	@r3exception
	async def run(self):
		try:
			if self.config.manager_settings is not None:
				if self.config.manager_settings['mode'] == 'CLIENT':
					self.manager_log_queue = asyncio.Queue()
				
			if self.config.startup is not None:
				if 'mode' in self.config.startup:
					if self.config.startup['mode'] == 'STANDARD':
						# starting in standalone mode...
						pass
					elif self.config.startup['mode'] == 'DEV':
						print('Starting in DEV mode!')
						os.environ['PYTHONASYNCIODEBUG'] = '1'
						os.environ['R3DEEPDEBUG'] = '1'
						self.loop.set_debug(True)

						# Make the threshold for "slow" tasks very very small for
						# illustration. The default is 0.1, or 100 milliseconds.
						self.loop.slow_callback_duration = 0.001

						# Report all mistakes managing asynchronous resources.
						warnings.simplefilter('always', ResourceWarning)

						# sys.settrace(tracefunc)

					elif self.config.startup['mode'] == 'TEST':
						os.environ['PYTHONASYNCIODEBUG'] = '1'
						os.environ['R3DEEPDEBUG'] = '1'
						if self.test_output_queue is None:
							self.test_output_queue = multiprocessing.Queue()
						if 'extensions' not in self.config.log_settings:
							self.config.log_settings['handlers'] = {}
						if 'TEST' not in self.config.log_settings['handlers']:
							self.config.log_settings['handlers']['TEST'] = 'TEST'
						if 'TEST' not in self.config.log_settings:
							self.config.log_settings['TEST'] = {}
						if 'output_queue' not in self.config.log_settings['TEST']:
							self.config.log_settings['TEST']['output_queue'] = self.test_output_queue

					elif self.config.startup['mode'] == 'SERVICE':
						if 'pidfile' not in self.config.startup['settings']:
							raise Exception('pidfile MUST be set when running in service mode')
						handle_systemd(self.config.startup['settings']['pidfile'])

				else:
					# starting in standalone mode...
					pass
			else:
				# starting in standalone mode...
				pass

			self.logprocessor = LogProcessor(self.config.log_settings, self.log_queue, manager_log_queue = self.manager_log_queue)
			self.loop.create_task(self.logprocessor.run())

			for serverconfig in self.get_serverconfigs():
				await self.start_server_task(serverconfig)
				
			await self.start_manager()

			await self.logger.info('Started all servers')
			#self.loop.run_forever()
			await self.shutdown_evt.wait()

		except KeyboardInterrupt:
			await self.logger.warning('CTRL+C pressed, exiting!')
			sys.exit(0)


class Responder3Config:
	CONFIG_OS_KEY = 'R3CONFIG'

	def __init__(self):
		self.startup = None
		self.log_settings = None
		self.server_settings = None
		self.manager_settings = None

	@staticmethod
	def from_dict(config):
		conf = Responder3Config()
		conf.startup = config['startup']
		conf.log_settings = config['logsettings']
		conf.server_settings = config['servers']
		if 'remote_manager' in config:
			conf.manager_settings = config['remote_manager']
		return conf

	@staticmethod
	def from_json(config_data):
		return Responder3Config.from_dict(json.loads(config_data))

	@staticmethod
	def from_file(file_path):
		with open(file_path, 'r') as f:
			config = json.load(f)
		return Responder3Config.from_dict(config)

	@staticmethod
	def from_python_script(file_path):
		loader = importlib.machinery.SourceFileLoader('responderconfig', file_path)
		spec = importlib.util.spec_from_loader(loader.name, loader)
		responderconfig = importlib.util.module_from_spec(spec)
		loader.exec_module(responderconfig)
		conf = Responder3Config()
		conf.startup = responderconfig.startup
		conf.log_settings = responderconfig.logsettings
		conf.server_settings = responderconfig.servers
		conf.manager_settings =  getattr(responderconfig, 'remote_manager', None) 

		return conf

	@staticmethod
	def from_os_env():
		config_file = os.environ.get(Responder3Config.CONFIG_OS_KEY)
		if config_file is None:
			raise Exception(
				'Could not find configuration file path in os environment variables!'
				'Name to be set: %s' % Responder3Config.CONFIG_OS_KEY
			)
		return Responder3Config.from_python_script(config_file)
