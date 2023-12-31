const quotes = [
    "Prepare your words, for the battle of wit is about to begin!",
    "In the realm of language, champions are born. Are you ready to conquer?",
    "Unleash your lexicon prowess! The word war awaits your mastery.",
    "Harness the power of words, and let the linguistic showdown commence!",
    "The pen is mightier than the sword, and you are the writer of your victory!",
    "Unravel the secrets of words, and you shall reign as a true WordWarrior!",
    "A symphony of letters awaits your command. Let the word battle begin!",
    "In this word arena, only the craftiest wordsmiths emerge victorious.",
    "Venture into the lexicon labyrinth and forge your path to triumph!",
    "The dictionary is your arsenal, and your wit is your sword.",
    "The battleground is set, and the pen shall be your weapon of choice.",
    "Words hold the power to unite, inspire, and conquer hearts.",
    "Let eloquence be your shield and vocabulary be your strength.",
    "Within each word lies a world waiting to be discovered. Dive in!",
    "Wield the magic of language and unleash the spellbinding verbiage.",
    "Dare to defy the limits of language and create your masterpiece.",
    "Like a maestro of words, compose the sonata of your linguistic triumph.",
    "In this realm of vocabulary, you are the orchestrator of destiny.",
    "Embark on this word odyssey, and let the epic language adventure begin!",
    "Unlock the treasure chest of words and claim your linguistic bounty.",
    "The battleground is not of steel but of syllables, and victory is within reach.",
    "Every word is a brushstroke in the painting of your word conquest.",
    "Immerse yourself in the symphony of language and become its virtuoso.",
    "Breathe life into letters, and they shall dance to your lyrical command.",
    "Assemble your lexicon army, for the battle of words is upon us!"
];

const countdownElem = $('#countdown');
const countdownContainer = $('#countdown-container');
const chatSection = $('#chat-section');
const input = $('#text-input')

// typing effects


$("#nameModal").on("hidden.bs.modal", function () {
    // put your default event here
    startCount()
});

// JavaScript code for pulsating animation
function startPulsating() {
    const countdown = $('#countdown');
    countdown.addClass('pulsate');
}

function stopPulsating() {
    const countdown = $('#countdown');
    countdown.removeClass('pulsate');
}


function displayRandomQuote() {
    const quoteElement = document.getElementById('quote');
    const randomIndex = Math.floor(Math.random() * quotes.length);
    quoteElement.textContent = quotes[randomIndex];
}

function startCount() {
    countdownTimer();
    displayRandomQuote(); // Display a random quote before the countdown
    setTimeout(() => {
        startPulsating();
        setTimeout(stopPulsating, 5000); // Stop pulsating after 5 seconds (or the desired countdown duration)
    }, 1000); // Delay the start of pulsating for 3 seconds (or the desired quote display duration)
}


function countdownTimer() {
    // Countdown timer
    let count = 5;
    const countdownInterval = setInterval(() => {
        countdownElem.text(count);
        count--;
        if (count < 0) {
            $('#lobby-section').show();
            countdownContainer.hide();
            $('#chat-message').focus();
            clearInterval(countdownInterval);
        }
    }, 1000);
}


function startGame() {
    // Code to start the game, initialize WebSocket connection, etc.
    // Implement user authentication if required.
}

function verifyUsername(url) {
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'JSON',
        data: {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'username': $('#modal-username').val(),
            'password': $('#modal-password').val(),
            'next': $('#next').val()
        },
        success: function (resp) {
            if (resp.status === 'success') {
                console.log(resp);
                var next = resp.next
                $('#loginModal').modal('hide');
                setTimeout(() => {
                    window.location.href = next
                }, 1000)
            }
            if (resp.status === 'error') {
                $('#login-error').text(resp.error)
            }
        },
        error: function () {
            console.log('error occured')
        }
    })
}

function registerUser(url) {
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'JSON',
        data: {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'username': $('#register-username').val(),
            'password': $('#register-password').val(),
            'confirm-password': $('#confirm-password').val()
        },
        success: function (resp) {
            if (resp.status === 'success') {
                var next = resp.next
                $('#loginModal').modal('hide');
                setTimeout(() => {
                    window.location.href = next
                }, 1000)
            }
            if (resp.status === 'error') {
                $('#registration-error').text(resp.error)
            }
        },
        error: function (resp) {
            console.log('error occured')
        }
    })
}
