/* Variables */
var body = $('body');
var scheme = body.data('scheme')
var host = body.data('host')
var protocol = scheme === 'http' ? 'ws://' : 'wss://'

var currentPath = window.location.href
var parts = currentPath.split('/')
var lobbyID = parts[parts.length - 1]

const url = protocol + host + '/ws/lobby/'+ lobbyID + '/'
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
socket.onopen = function (event) {
    console.log('connection success... ', url);
}


socket.onclose = function (event) {
    console.log('disconnected...')
}

socket.onmessage = function (event) {
    console.log('event: ', event);
    const dataObj = JSON.parse(event.data)
    const dataMessage = dataObj.data

    switch (dataObj.type){
        case 'player_joined':
            const image = dataMessage.image
            var message = dataMessage.message
            console.log('message: ', message);
            console.log('image: ', image);
            $('#player-list').append(image);
            break;
        case 'all_players':
            const images = dataMessage.images
            console.log('image: ', images);
            $('#player-list').html('').append(images);
            break;
    }
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


