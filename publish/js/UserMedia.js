var UserMedia = (function(){
	this.video = document.createElement('video');
	this.video.autoplay = true;
	
	// Success Callback
	var onUserMediaSuccess = function(mediaStream){
		this.video.src = window.URL.createObjectURL(mediaStream);
		this.mediaStream = mediaStream;
		console.log(mediaStream);
	};
	
	// Error Callback
	var onUserMediaError = function(mediaError){
		console.log("Rejected!",mediaError);
	};
	
	navigator.getUserMedia = navigator.getUserMedia ||
		navigator.webkitGetUserMedia ||
		navigator.mozGetUserMedia ||
		navigator.msGetUserMedia;
		
	navigator.getUserMedia({"video":true},onUserMediaSuccess,onUserMediaError);

	// UserMedia Object
	function oUserMedia(){};
	oUserMedia.prototype = {
		constructor:UserMedia,
		video:this.video,
		snapshot:function(type){
			var canvas = document.createElement("canvas",{preserveDrawingBuffer:true});
			canvas.width=this.video.videoWidth;
			canvas.height=this.video.videoHeight;
			
			var context = canvas.getContext("2d");
			context.drawImage(this.video,0,0);
			
			return canvas.toDataURL('image/png');
		},
		snapshotBlob:function(type){
	        var srcData = this.snapshot(type);
			var imgData = srcData.split(',')[1];
    		var byteString = atob(imgData);
    		var buffer = new Uint8Array(byteString.length);
    		
    		for(var i=0;i<byteString.length;i++){
    			buffer[i] = byteString.charCodeAt(i);
    		}
			var blob = new Blob([buffer], {'type': type});
			return blob;
		},
		getStream:this.mediaStream,
	};
	return oUserMedia;
})();
