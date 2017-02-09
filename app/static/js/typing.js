var b = 0;
var c = 0;
var isTyping = true;
var isLoop = true;
var i = 0;
var typingSpeed = 100;
var deleteSpeed = 40;
setTimeout("typing()", 800);

function typing() {
	document.getElementById("words").innerHTML = strings[i].substring(c, b);
	if (b == strings[i].length){
	    setTimeout("b=0, c=strings[i].length, isTyping=true",800);
	} else {
		if (c != 0) {
			c--;
			if ((i == strings.length-1) && (isLoop==false)) {
				return;
			}

			if (c == 0) {
				i++;
				if (i == strings.length) {
					i=0;
				}
			}
		} else {
			var isTyping=false;
			b++;
			}
	}

	if (isTyping == false) {
		setTimeout("typing()", typingSpeed);
	} else {
		setTimeout("typing()", deleteSpeed);
	}
}