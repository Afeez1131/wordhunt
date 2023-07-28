/* Variables */
var body = $('body');
var scheme = body.data('scheme')
var host = body.data('host')
console.log(scheme, host);
var protocol = scheme === 'http' ? 'ws://' : 'wss://'
const url = protocol + host + '/ws/game/'
console.log(url);
const socket = new WebSocket(url);

socket.onopen = function () {
    console.log('connection success...');
}

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    console.log(data);
    switch (data.action) {
        case "connected":
            $('p#connected').text(data.message)
            break;
        case "time":
            $('p#time').text(data.message);
            break;
    }
}

// Submit button click effect
const submitButton = $('#submit-button');
submitButton.click(function () {
    // Implement the action to be performed when the submit button is clicked.
    // For example, sending the word to the backend for validation and updating chat messages.
    addText();
});

function addText() {
    var inputText = input.val();
    if (inputText !== '') {
        var temp = `<div class="other-user-message">
                <div class="message-text">
                    <span class="user-name">Mary:</span> ${inputText}
                    <span class="message-time">10:20 AM</span>
                </div>
            </div>`
        $('#chat-messages').append(temp);
    }
    scrollToBottom();

}

function scrollToBottom() {
    const chatMessages = document.getElementById('chat-messages');
    const lastMessage = chatMessages.lastElementChild;
    if (lastMessage) {
        lastMessage.scrollIntoView({behavior: 'smooth', block: 'end'});
    }
}
