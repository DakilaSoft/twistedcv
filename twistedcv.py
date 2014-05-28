import cv2
import cv2.cv as cv
import numpy as np
import base64

from twisted.internet import threads
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory

class DetectorServerProtocol(WebSocketServerProtocol):
	def onConnect(self,request):
		print("Client connecting: {0}".format(request.peer))
		
	def onOpen(self):
		print("WebSocket connection open.")
		
	def onClose(self, wasClean, code, reason):
		print("WebSocket connection closed: {0}".format(reason))
		
	def onMessage(self, payload, isBinary):
		if isBinary:
			print("Binary Message Received!")
			self.payload = payload;
			
			def sendImage(b64):
				self.sendMessage("data:image/jpeg;base64,"+b64)
				
			"""
			Run detection on background
			"""
			d = threads.deferToThread(self.factory.decodeByteArray,payload)
			d.addCallback(self.factory.detect)
			d.addCallback(self.factory.encodeBase64)
			d.addCallback(sendImage)
			
		else:
			print("Text Message Received!")
			
class DetectorServerFactory(WebSocketServerFactory):
	protocol = DetectorServerProtocol
	
	def __init__(self, cascade, port):
		self.cascade = cv2.CascadeClassifier(cascade)
		WebSocketServerFactory.__init__(self,"ws://localhost:"+str(port), debug=False)
		
	"""
	Decode Buffer Image
	"""
	def decodeByteArray(self, data):
		imgArr = np.frombuffer(data,dtype="uint8")
		return cv2.imdecode(imgArr,1)
		
	"""
	Object detection
	"""
	def detect(self,image):
		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		gray = cv2.equalizeHist(gray)
		
		rects = self.cascade.detectMultiScale(
			gray,
			scaleFactor=1.3,
			minNeighbors=4,
			minSize=(30, 30),
			flags=cv.CV_HAAR_SCALE_IMAGE
		)
		return self.drawRect(image,rects,(0,255,0))
		
	"""
	Draw rectangle on image with the detected object
	"""
	def drawRect(self,image,rects,color):
		if len(rects) == 0:
			return image
		
		rects[:,2:] += rects[:,:2]
		for x1, y1, x2, y2 in rects:
			cv2.rectangle(image, (x1,y1), (x2,y2), color, 2)
			
		return image

	"""
	Encode image to Base64
	"""
	def encodeBase64(self,image):
		encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
		_, buf = cv2.imencode(".jpg",image,encode_param)
		return base64.encodestring(buf.tostring())
		