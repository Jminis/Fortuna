// static/js/rank.js

function setupRankWebSocket() {
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/ws/rank/";
    var websocket = new WebSocket(ws_path);

    websocket.onopen = function (e) {
        console.log("Rank WebSocket connected!");
    };

    websocket.onmessage = function (e) {
        var data = JSON.parse(e.data);
        console.log("Received data:", data); // 이 부분 추가
        if (data.message === 'rank_data') {
            updateRankTable(data.data);
        }
    };

    websocket.onclose = function (e) {
        console.error("Rank WebSocket disconnected.");
    };

    websocket.onerror = function (e) {
        console.error("Rank WebSocket error: ", e.message);
    };
}

function updateRankTable(rankData) {
    var rankTableBody = document.getElementById("rank-table-body");
    rankTableBody.innerHTML = ""; // Clear existing rows

    rankData.forEach(function(team, index) {
        var row = rankTableBody.insertRow();
        var cellRank = row.insertCell(0);
        var cellName = row.insertCell(1);
        var cellScore = row.insertCell(2);

        cellRank.innerHTML = index + 1;
        cellName.innerHTML = team.name;
        cellScore.innerHTML = team.score;
    });
}

window.addEventListener("load", setupRankWebSocket);
