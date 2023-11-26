let socket = new WebSocket('ws://127.0.0.1:8000/ws/log/');

socket.onmessage = function(event) {
    console.log("Log WebSocket connected!");
    let data = JSON.parse(event.data);
    addMessageToPage(data.data);  // 서버로부터의 응답을 페이지에 표시
};


document.addEventListener('DOMContentLoaded', function () { //getElementById 전에 DOM을 먼저 로드해줘야 senbutton이 인식됨
    document.getElementById('sendButton').onclick = function() {
        console.log('버튼 클릭됨');
        let inputVal = document.getElementById('inputField').value;
        socket.send(JSON.stringify({data: inputVal}));
        document.getElementById('inputField').value = '';
    };
});


// function addMessageToPage(message) {
//     let messageList = document.getElementById('messageList');
//     let newMessageItem = document.createElement('li');
//     newMessageItem.textContent = message;
//     messageList.appendChild(newMessageItem);
// }

function addMessageToPage(message, timestamp) {
    let messageList = document.getElementById('messageList');

    // 메시지 컨테이너 생성
    let messageContainer = document.createElement('li');
    messageContainer.className = 'message-container';

    // 메시지 본문 생성
    let messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    messageDiv.textContent = message;

    // 시각 생성
    let timestampDiv = document.createElement('div');
    timestampDiv.className = 'timestamp';
    timestampDiv.textContent = timestamp; // 시각을 파라미터로 받거나 현재 시각을 설정

    // 컨테이너에 메시지와 시각 추가
    messageContainer.appendChild(messageDiv);
    messageContainer.appendChild(timestampDiv);

    // 메시지 리스트에 컨테이너 추가
    messageList.appendChild(messageContainer);
}
