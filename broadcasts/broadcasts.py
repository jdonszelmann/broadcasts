import socket
import time
import threading
import queue
import pickle
import colorama
colorama.init(autoreset=True)

class Sender(threading.Thread):
	senders = []

	def __init__(self,port):

		self.port = port

		super().__init__()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		# Set a timeout so the socket does not block
		# indefinitely when trying to receive data.
		self.sock.settimeout(0.2)
		self.sock.bind(("", 44444))

		self.queue = queue.PriorityQueue()

		self.__class__.senders.append(self)

		self.running = True
		self.start()

	def run(self):
		while self.running:
			if not self.queue.empty():
				message = self.queue.get()[1]
				self.sock.sendto(message, ('<broadcast>', self.port))

	def stop(self):
		while not self.queue.empty():
			print(colorama.Fore.RED + "exiting thread {}...."
				" waiting for queue to empty. size: {}"
				.format(threading.get_ident(),self.queue.qsize())
			)
			time.sleep(0.1)
		print()

		self.running = False
		self.join()

	def send(self,obj,priority=999):
		data = pickle.dumps(obj)
		self.queue.put((priority,data))

	@classmethod
	def stopall(cls):
		for i in cls.senders:
			i.stop()

class Receiver(threading.Thread):
	receivers = []
	
	def __init__(self,address,port,recvfunc):
		super().__init__()
		self.port = port
		self.address = address

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.settimeout(0.2)
		self.sock.bind((address, int(port)))

		self.recvfunc = recvfunc

		self.__class__.receivers.append(self)

		self.running = True
		self.start()

	def run(self):
		while self.running:
			try:
				data, addr = self.sock.recvfrom(1024*4)
				self.recvfunc(pickle.loads(data),addr)
			except socket.timeout:
				pass
			except:
				raise


	def stop(self):
		self.running = False
		self.join()

	@classmethod
	def stopall(cls):
		for i in cls.senders:
			i.stop()