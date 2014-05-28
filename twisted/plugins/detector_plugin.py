from zope.interface import implements

from twisted.application.service import IServiceMaker
from twisted.application import internet
from twisted.plugin import IPlugin
from twisted.python import usage

from twistedcv import DetectorServerFactory

class Options(usage.Options):
	optParameters = [
		["port","p",9000,"The port number to listen on."],
		["cascade","c","classifier/haarcascade_frontalface_alt.xml","The classifier use for detection."]
	]
	
class DetectorServiceMaker(object):
	implements(IServiceMaker, IPlugin)
	tapname = "twistedcv"
	description = "A Object Detection Server"
	options = Options
	
	def makeService(self, options):
		factory = DetectorServerFactory(options["cascade"],int(options["port"]))
		return internet.TCPServer(int(options["port"]),factory)
		
serviceMaker = DetectorServiceMaker()