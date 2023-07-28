/* Variables */
var body = $('body');
var scheme = body.data('scheme')
var host = body.data('host')
var protocol = scheme === 'http' ? 'ws://' : 'wss://'
const url = protocol + host + '/ws/lobby/afeez/'
const inputText = $('#chat-message');
const sendButton = $('#send-button');

const socket = new WebSocket(url);

$(document).ready(function() {
    // Handle Enter key press on the input field
    inputText.focus();
    inputText.on('keydown', function (event) {
        if (event.keyCode === 13) { // 13 is the keycode for Enter key
            sendChat();
        }
    });
})
socket.onopen = function () {
    console.log('connection success...');
}


function sendData(message, socket) {
    socket.send(JSON.stringify(message));
}

sendButton.click(() => {
    sendChat();
})

function sendChat() {
    var text = inputText.val();
    const data = {
        'text': text
    }
    sendData(data, socket);
}


