import sys

from twisted.python import log
from twisted.internet import reactor

from twistedcv import DetectorServerFactory
				
log.startLogging(sys.stdout)
factory = DetectorServerFactory("classifier/haarcascade_frontalface_alt.xml",9000)
reactor.listenTCP(9000,factory)
reactor.run()
