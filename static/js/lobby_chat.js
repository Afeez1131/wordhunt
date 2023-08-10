/* Variables */
const body = $('body');
const scheme = body.data('scheme')
const host = body.data('host')
const protocol = scheme === 'http' ? 'ws://' : 'wss://'

const currentPath = window.location.href
const parts = currentPath.split('/')
const lobbyID = parts[parts.length - 1]

const url = protocol + host + '/ws/lobby/' + lobbyID + '/'
const inputText = $('#chat-message');
const sendButton = $('#send-button');

const socket = new WebSocket(url);


$(document).ready(function () {
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
    console.log('trying to reconnect...')
    setTimeout(connect, 3000);
}

socket.onerror = function (event) {
    console.log('error occured', event);
}

socket.onmessage = function (event) {
    console.log('event: ', event);
    const dataObj = JSON.parse(event.data)
    const dataMessage = dataObj.data
    const player_list = $('#player-list')
    const chatBox = $('#chat-box');

    switch (dataObj.type) {
        case 'player_joined':
            const image = dataMessage.image
            var message = dataMessage.message
            var player = dataMessage.joined_user
            console.log(username, player);
            player_list.append(image);
            break;
        case 'all_players':
            const images = dataMessage.images
            player_list.html('').append(images);
            break;
        case 'echo_message':
            if (username === dataMessage.sender) {
                chatBox.append(dataMessage.message_sender);
            } else {
                chatBox.append(dataMessage.message_receiver);
            }
            scrollToBottom();
            break;
        case 'join_chat_alert':
            player = dataMessage.player
            message = dataMessage.message
            if (username !== player) {
                $('#chat-box').append(message);
            }
            scrollToBottom();
            break;
        case 'left_chat_alert':
            player = dataMessage.player
            message = dataMessage.message
            if (username !== player) {
                chatBox.append(message);
            }
            scrollToBottom();
            break;
        case 'start_game':
            let url = dataMessage.game_room;
            setTimeout(() => {
                window.location.href = url
            }, 1000);
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
        'action': 'new_message',
        'data': {
            'message': text,
            'sender': username
        }
    }
    inputText.val('');
    sendData(data, socket);
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


/*  emoji   */
$(document).ready(() => {
    const emojis = ['😀', '😄', '😊', '😃', '👍', '👋', '❤️', '😎', '🥳', '🌞', '😁',
        '😆', '😅', '😂', '🤣', '😇', '😍', '😘', '😋', '😜', '😝', '😏', '😌', '😊',
        '😉', '🙃', '🙂', '😶', '😐', '😑', '😒', '😬', '🙄', '😳', '😞', '😟', '😔',
        '😕', '🙁', '☹️', '😣', '😖', '😫', '😩', '😢', '😭', '😤', '😠', '😡', '🤬',
        '🤯', '😳', '🥺', '😨', '😰', '😥', '😓', '🤗', '🤔', '🤭', '🤥', '😶',
        '😐', '😑', '😬', '🙄', '😯', '😦', '😧', '😮', '😲', '😴', '🤤', '😪', '😵']

    const emojiContainer = $('#emoji-container')
    emojis.forEach(emoji => {
        const emojiButton = $('<button>').addClass('emoji-option').text(emoji);
        emojiContainer.append(emojiButton);
    })

    $('.emoji-option').click(function () {
        const emoji = $(this).text();
        const cursorPos = inputText[0].selectionStart;
        const inputVal = inputText.val()
        const beforeCursor = inputVal.slice(0, cursorPos)
        const afterCursor = inputVal.slice(cursorPos)
        const newValue = beforeCursor + emoji + afterCursor;
        inputText.val(newValue);
        inputText.focus();
    })
})


const startGameButton = $('#start-button')
startGameButton.click(function () {
    console.log('clicked start game button');
    const message = {
        'action': 'start_game',
    }
    sendData(message, socket);
})
