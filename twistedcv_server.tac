from twisted.application import internet, service
from twistedcv import DetectorServerFactory

application = service.Application("twistedcv")
factory = DetectorServerFactory('classifier/haarcascade_frontalface_alt.xml',9000)
service = internet.TCPServer(9000,factory)
service.setServiceParent(application)
