let url = 'ws://'+window.location.host + '/ws/chat/room/' + '{{ course.id }}/';
let chatSocket = new WebSocket(url)
// Code for when message is received
chatSocket.onmessage = function(e){
    let data = JSON.parse(e.data);
    let message = data.message;

    let $chat = $('#chat');
    $chat.append('<div class="message">' + message + '</div>');
    $chat.scrollTop($chat[0].scrollHeight);
};
chatSocket.onclose = function(e){
    console.error('Chat socket closed unexpectedly')
}

// Code for when use reply in the browser
let $input = $('#chat-message-input');
let $submit = $('#chat-message-submit');

$submit.click(function(){
    let message = $input.val();
    if(message){
        // send message in Json format
        chatSocket.send(JSON.stringify({'message': message}));

        //clear message window
        $input.val('');

        // return focus on the message window
        $input.focus();
    }
});

// When the page loads the focus has to be on the input
// so user can type message
$input.focus();
$input.keyup(function(e){
    if(e.which === 13){
        // submit with enter/ return key
        $submit.click();
    }
})