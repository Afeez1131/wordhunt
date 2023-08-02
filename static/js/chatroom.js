/* Variables */
const body = $('body');
const scheme = body.data('scheme')
const host = body.data('host')
const path_name = window.location.pathname.split('/')
const room_name = path_name[path_name.length - 1]
const protocol = scheme === 'http' ? 'ws://' : 'wss://'
const url = protocol + host + '/ws/game/'+ room_name + '/'
const chatBox = $('#chat-box')
const socket = new WebSocket(url);

socket.onopen = function () {
    console.log('connection success...');
}

socket.onmessage = function (event) {
    console.log('event: ', event);
    const data = JSON.parse(event.data);
    const dataMessage = data.data;
    switch (data.type) {
        case "connected":
            $('p#connected').text(data.message)
            break;
        case "game_rule":
            let rule = dataMessage.rule_template
            // chatBox.prepend(rule);
        case "echo_user_response":
            let sender = dataMessage.sender;
            if (sender === user) {
                chatBox.append(dataMessage.sender_template);
            } else {
                chatBox.append(dataMessage.receiver_template);
            }
            scrollToBottom();
            break;
    }
}

// Submit button click effect
const submitButton = $('#send-button');
const inputText = $('#player-message')

submitButton.click(function () {
    console.log('clicked submit button');
    let text = inputText.val();
    const msg = {
        'action': 'player_message',
        'data': {
            'message': text,
            'sender': user
        }
    }
    inputText.val('');
    sendData(msg, socket);
});

function sendData(message, socket) {
    socket.send(JSON.stringify(message))
}

function scrollToBottom() {
    // Get the chat container element
    const chatContainer = $(".chat-box");

    // Calculate the distance to scroll
    const scrollHeight = chatContainer[0].scrollHeight;
    console.log('height: ', scrollHeight);

    // Animate the scrolling to the bottom
    chatContainer.animate({scrollTop: scrollHeight}, 'slow');
}

$(document).ready(function() {
    inputText.focus();
    inputText.on('keydown', function(event) {
        if (event.keyCode === 13) {
            submitButton.click();
        }
    })
})
