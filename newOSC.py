'''
need to implement the following functions
initOSCClient(host, port) - starts a osc client
initOSCServer(host, port) - starts a osc server
closeOSC() - stops both client and server
setOSCHandler(addr,func) - adds a msg dispatcher to server
sendOSCMsg(addr,data) - send an osc message
'''
import threading
from pythonosc import dispatcher, osc_server, osc_message_builder, udp_client

class TouchLiveOscBackend:
	def __init__(self):
		self.dispatcher = dispatcher.Dispatcher()
		self.client = None


	def initOSCClient(self, ip='127.0.0.1', port=9000):
		self.client = udp_client.UDPClient(ip, port)

	def initOSCServer(self, ip='127.0.0.1', port=9001):
		self.server = osc_server.ThreadingOSCUDPServer((ip, port), self.dispatcher)
		self.server_thread = threading.Thread(target=self.server.serve_forever)
		self.server_thread.start()

	def closeOSC(self):
		self.server.shutdown()
		self.server_thread.join()

	def setOSCHandler(self,addr,func):
		self.dispatcher.map(addr,func)

	def sendOSCMsg(self,addr='/print',data=[]):
		if self.client is not None:
			msg = osc_message_builder.OscMessageBuilder(address = addr)
			for d in data:
				msg.add_arg(d)
			msg = msg.build()
			self.client.send(msg)

if __name__ == '__main__':
	test = TouchLiveOscBackend()
	test.initOSCClient()
	test.initOSCServer()
	def printing_handler(addr,tags,data,source):
		print("---")
		print("received new osc msg from %s" % getUrlStr(source))
		print("with addr : %s" % addr)
		print("typetags :%s" % tags)
		print("the actual data is : %s" % data)
		print("---")
	test.setOSCHandler('/print',printing_handler)
	test.sendOSCMsg()
	test.closeOSC()