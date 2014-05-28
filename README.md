TwistedCV
=====
TwistedCV is a Web-Based implementation of OpenCV. TwistedCV uses browser WebRTC MediaStream to send video frame to WebSocket server and process the frame for object detection and send back the frame to the browser.

Requirements
=====
* OpenCV with Python support *http://opencv.org/*
* Twisted Networking Engine *http://twistedmatrix.com*
* Autobahn Websocket *http://autobahn.ws/*

Usage
=====
To start the server one of the following command:

python twistedcv_server.py

or

twistd -ny twistedcv_server.tac

or

twistd twistedcv [--cascade=classifier/haarcascade_frontalface_alt.xml --port=9000]

and for the client, navigate to the url below:

*http://localhost/twistedcv/publish/*

Live Demo
=====
*http://project.di9itdm9.com/twistedcv/publish/*
