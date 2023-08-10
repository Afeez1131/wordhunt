/* Variables */
const body = $('body');
const scheme = body.data('scheme')
const host = body.data('host')
const path_name = window.location.pathname.split('/')
const room_name = path_name[path_name.length - 1]
const protocol = scheme === 'http' ? 'ws://' : 'wss://'
const url = protocol + host + '/ws/game/'+ room_name + '/?1'
const chatBox = $('#chat-box')
const socket = new WebSocket(url);

socket.onopen = function () {
    console.log('connection success...', url);
}

socket.onmessage = function (event) {
    // console.log('event: ', event);
    const data = JSON.parse(event.data);
    console.log('data: ', data);
    switch (data.type) {
        case "connected":
            $('p#connected').text(data.message)
            break;
        case "game_rule":
            let rule = data.rule_template
            // chatBox.prepend(rule);
            break;
        case "echo_user_response":
            let sender = data.sender;
            if (sender === user) {
                chatBox.append(data.sender_template);
            } else {
                chatBox.append(data.receiver_template);
            }
            scrollToBottom();
            break;
        case "countdown":
            let count = data.countdown;
            // if
            chatBox.html('<span class="notification" id="notification">\n' +
                '   <h3>' + count + '</h3>\n' +
                '</span>\n')
    }
}

// Submit button click effect
const submitButton = $('#send-button');
const inputText = $('#player-message')

submitButton.click(function () {
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
