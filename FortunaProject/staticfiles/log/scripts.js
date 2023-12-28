// WebSocket 연결
let socket = new WebSocket('ws://127.0.0.1:8000/ws/log/');

socket.onmessage = function(event) {
    let data = JSON.parse(event.data);
    addMessageToPage(data.data);
};

document.getElementById('sendButton').onclick = function() {
    let inputVal = document.getElementById('inputField').value;
    socket.send(JSON.stringify({data: inputVal}));
};

function addMessageToPage(message) {
    let messageList = document.getElementById('messageList');
    let newMessageItem = document.createElement('li');
    newMessageItem.textContent = message;
    messageList.appendChild(newMessageItem);
}

