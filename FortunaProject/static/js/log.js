let socket = new WebSocket('ws://127.0.0.1:8000/ws/log/');

socket.onmessage = function(event) {
    console.log("Log WebSocket connected!");
    let data = JSON.parse(event.data);
    
    if (data.toast) {
        showToast(data.toast);
    } else {
        addMessageToPage(data.data);
    }

};


document.addEventListener('DOMContentLoaded', function () { //getElementById 전에 DOM을 먼저 로드해줘야 senbutton이 인식됨
    document.getElementById('sendButton').onclick = function() {
        console.log('버튼 클릭됨');
        let inputVal = document.getElementById('inputField').value;

        // 토스트 메시지 표시
        showToast("메시지 전송: " + inputVal);

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

function showToast(message) {
    let toast = document.createElement("div");
    toast.className = "toast-message";
    toast.textContent = message;

    // 왼쪽 컬럼의 첫 번째 요소를 선택
    let leftColumn = document.getElementById('leftColumn');
    if (leftColumn) {
        // 왼쪽 컬럼의 가장 상단에 토스트 메시지 추가
        leftColumn.insertBefore(toast, leftColumn.firstChild);
    } else {
        console.error('Left column not found');
        return;
    }

    toast.classList.add("show");

    setTimeout(function(){ 
        toast.classList.remove("show");
        toast.remove();
    }, 3000);
}