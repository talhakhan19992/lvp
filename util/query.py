import socket;

class SAMPInfoRequest:
	
	def __init__(self, ip, port):
		self.ip    = ip;
		self.port  = port;
		self.error = False;
		
		packet = self.build_packet();
		self.request(packet);
		
		
	def parse(self, data):
		
		data = data[11:];
		
		self.passworded  = bool(data[0])
		self.players     = (data[2] << 8) | data[1];
		self.max_players = (data[4] << 8) | data[3];
		
		hname_len = (data[8] << 24) | (data[7] << 16) | (data[6] << 8) | data[5];
		
		self.hostname = (data[9:(9 + hname_len)]).decode("UTF-8");
	
	def request(self, packet):
	
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
		sock.settimeout(3);
		
		try:
			sock.sendto(packet, (self.ip, self.port));
			
			data = sock.recv(1024);
			self.parse(data);
			
		except Exception:
			self.error = True;
		

	def build_packet(self):
		packet = [ord(c) for c in "SAMP"];

		packet.extend([ int(x) for x in self.ip.split(".") ]);
		packet.extend([ self.port & 0xff, (self.port >> 8) & 0xff ]);
		packet.append(ord('i'));

		return bytes(packet);

		
class VCMPInfoRequest:
	
	def __init__(self, ip, port):
		self.ip    = ip;
		self.port  = port;
		self.error = False;
		
		packet = self.build_packet();
		self.request(packet);
		
		
	def parse(self, data):
		
		data = data[11:];
		
		self.version        = data[0:11].decode("UTF-8");
		self.passworded     = bool(data[12]);
		self.players        = (data[14] << 8) | data[13];
		self.max_players    = (data[16] << 8) | data[15];
	
	def request(self, packet):
	
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
		sock.settimeout(3);
		
		try:
			sock.sendto(packet, (self.ip, self.port));
			
			data = sock.recv(1024);
			self.parse(data);
			
		except Exception:
			self.error = True;
		

	def build_packet(self):

		packet = [ord(c) for c in "VCMP"];
		opcode = 'i';

		packet.extend([int(block) for block in self.ip.split('.')])
		packet.extend([self.port & 0xff, (self.port >> 8) & 0xff, ord(opcode)]);

		packet = bytearray(packet);
		
		return packet;


