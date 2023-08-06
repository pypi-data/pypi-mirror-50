import platform
import ipaddress
import socket
from responder3.core.sockets import SocketConfig

from responder3.core.interfaces.darwin import get_darwin_ifaddrs
from responder3.core.interfaces.linux import get_linux_ifaddrs
from responder3.core.interfaces.windows import get_win_ifaddrs

class NetworkInterfaces:
    def __init__(self):
        """
        Provides a platform-independent way of enumerating all available interfaces and IP addresses on the host
        """
        self.interfaces = self.enumerate_interfaces()
        self.name_ip_lookup = {}
        self.ip_name_lookup = {}
        self.iface_help = ''
        
        # creating lookup tables, and help string to display on help menu
        self.generate_lookups_and_help(self.interfaces)

    def enumerate_interfaces(self):
        """
        Enumerates all interfaces on host
        :return: None
        """
        if platform.system() == 'Windows':
            return get_win_ifaddrs()
        if platform.system() == 'Linux':
            return get_linux_ifaddrs()
        if platform.system() == 'Darwin':
            return get_darwin_ifaddrs()

    def store_ip_for_interface(self, iface, ip):
        if (iface, ip.version) not in self.name_ip_lookup:
            self.name_ip_lookup[(iface, ip.version)] = []
        self.name_ip_lookup[(iface, ip.version)].append(ip)

    def store_interface_to_ip(self, iface, ip):
        if ip in self.ip_name_lookup:
            print('Multiple interface found with the same IPv4 address! You will need to specify interface name in config')
            return
        self.ip_name_lookup[ip] = iface

    def generate_lookups_and_help(self, interfaces):
        """
        Generates lookup dictionaries and a formatted string describing all interfaces and addresses
        :return: None
        """
        self.iface_help += 'NAME\tIPv4\t\tIPv6\r\n'
        for iface in interfaces:
            addresses = [str(ip) for ip in interfaces[iface].addresses]
            self.iface_help += '\t'.join([iface, ','.join(addresses), '\r\n'])

            for ip in interfaces[iface].addresses:
                self.store_ip_for_interface(iface, ip)
                self.store_interface_to_ip(iface, ip)

    def get_ifname(self, ip):
        """
        Returns interface name belonging to the IP address provided in ip
        :param ip: IP address to search the interface for
        :type ip: ipaddress.IPv4Address or ipaddress.IPv6Address
        :return: str
        """
        return self.ip_name_lookup.get(str(ip), None)

    def get_ip(self, ifname, ipversion = 4):
        """
        Returns version 4 or 6 ip addresses for the interface specified by ifname.
        :param ifname: Name of the interface
        :type ifname: str
        :param ipversion: Specified ip address version to return
        :type ipversion: int
        :return: list
        """
        return self.name_ip_lookup.get((ifname, ipversion), None)

    def get_socketconfig_from_ip(self, ip, port, protocol):
        """
        Returns a SocketConfig object for the given ip, port, protocol
        :param ip: IP address belonging to an existing interface
        :param port: port numer
        :param protocol: protocol type
        :type protocol: socket.SOCK_STREAM or socket.SOCK_DGRAM
        :return: SocketConfig
        """
        sc = SocketConfig()
        sc.bind_port = int(port)
        if isinstance(ip, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
            sc.bind_addr = ip
        else:
            sc.bind_addr = ipaddress.ip_address(ip)

        sc.bind_family = sc.bind_addr.version

        if isinstance(protocol, str):
            if protocol.lower() == 'tcp':
                sc.bind_protocol = socket.SOCK_STREAM
            elif protocol.lower() == 'udp':
                sc.bind_protocol = socket.SOCK_DGRAM
            else:
                raise Exception('Unknown protocol definition %s' % protocol)
        elif isinstance(protocol, int):
            sc.bind_protocol = protocol
        else:
            raise Exception('Unknown protocol definition %s' % protocol)

        sc.bind_iface = self.ip_name_lookup[sc.bind_addr]
        sc.bind_iface_idx = self.interfaces[sc.bind_iface].ifindex

        return sc

    def get_ivs(self, ipversion):
        if ipversion is None:
            return [4, 6]
        if isinstance(ipversion, list):
            return ipversion
        if int(ipversion) in [4,6]:
             return [int(ipversion)]
        else:
            raise Exception('Unknown IP version %s' % repr(ipversion))

    def get_protocol(self, protocol):
        if isinstance(protocol, int):
            return protocol
        if isinstance(protocol, str):
            if protocol.lower() == 'tcp':
                return socket.SOCK_STREAM
            elif protocol.lower() == 'udp':
                return socket.SOCK_DGRAM
        raise Exception('Unknown protocol definition %s' % protocol)

    def get_sc(self, ifname, address, port, protocol, server):
        sc = SocketConfig()
        sc.bind_port = int(port)
        sc.bind_addr = address
        sc.bind_family = sc.bind_addr.version
        sc.bind_protocol = self.get_protocol(protocol)
        sc.bind_iface = ifname
        sc.bind_iface_idx = self.interfaces[sc.bind_iface].ifindex
        sc.is_server = server
        return sc

    def get_client_socketconfig(self, ifname, protocol, ipversion = None, reuse_address = False, reuse_port= False):
        if ifname not in self.interfaces:
            raise Exception('Could not find ifname %s!' % ifname)

        scl = []

        for version in self.get_ivs(ipversion):
            for lookup_ifname, ver in self.name_ip_lookup:
                if ifname != lookup_ifname:
                    continue
                if ver != version:
                    break
                for address in self.name_ip_lookup[(lookup_ifname, ver)]:
                    sc = self.get_sc(ifname, address, 0, protocol, False)
                    sc.reuse_address = reuse_address
                    sc.reuse_port = reuse_port
                    scl.append(sc)

        return scl
       
    def get_socketconfig(self, ifname, port, protocol, ipversion = None):
        """
        Returns a list of socketconfig objects to create server.
        :param ifname: Interface name
        :type ifname: str
        :param port: Port number
        :type port: int
        :param protocol: Protocol type
        :type protocol: str or int or socket.SOCK_STREAM/socket.SOCK_DGRAM
        :param ipversion: IP address version
        :return: list of SocketConfig
        """
        if ifname not in self.interfaces:
            raise Exception('Could not find ifname %s!' % ifname)

        scl = []

        for lookup_ifname, ver in self.name_ip_lookup:
            for version in self.get_ivs(ipversion):
                if ifname != lookup_ifname:
                    continue
                if ver != version:
                    break
                for address in self.name_ip_lookup[(lookup_ifname, ver)]:
                    sc = self.get_sc(ifname, address, port, protocol, True)
                    scl.append(sc)

        return scl

    def __str__(self):
        return self.iface_help

interfaces = NetworkInterfaces()

