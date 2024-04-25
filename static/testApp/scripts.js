// サーバーから終了時間を取得する関数
async function fetchEndTime() {
    try {
        const response = await fetch('/api/endTime');
        const responseJson = await response.json();
        console.log(`Fetched end time text: ${responseJson.time}`);
        const endTime = new Date(responseJson.time);
        console.log(`Fetched end time: ${endTime}`);
        return endTime;
    } catch (error) {
        console.error(`Error fetching end time: ${error}`);
    }
}
async function fetchReservationTimes(scheduleId) {
    try {
        const response = await fetch(`/api/reservationTimes/${scheduleId}`);
        const responseJson = await response.json();
        const startTime = new Date(responseJson.startTime);
        const endTime = new Date(responseJson.endTime);
        return { startTime, endTime };
    } catch (error) {
        console.error(`Error fetching reservation times: ${error}`);
    }
}

/// サーバーから現在時間を取得し、タイマーを更新する関数
async function updateTimerDisplay(endTime, timerWorker) {
    try {
        const response = await fetch('/api/currentTime');
        const responseJson = await response.json();
        const now = new Date(responseJson.time);

        const remainingTime = endTime - now > 0 ? endTime - now : 0;
        console.log(`Remaining time (in milliseconds): ${remainingTime}`);

        const seconds = Math.floor((remainingTime / 1000) % 60);
        console.log(`Seconds: ${seconds}`);

        const minutes = Math.floor((remainingTime / 1000 / 60) % 60);
        console.log(`Minutes: ${minutes}`);

        const hours = Math.floor((remainingTime / (1000 * 60 * 60)) % 24);
        console.log(`Hours: ${hours}`);

        const days = Math.floor(remainingTime / (1000 * 60 * 60 * 24));
        console.log(`Days: ${days}`);

        const timerElement = document.getElementById('timer');
        const newContent = `${days} days, ${hours} hours, ${minutes} minutes, ${seconds} seconds remaining`;
        timerElement.textContent = newContent;
    } catch (error) {
        console.error(`Error fetching current time: ${error}`);
    }
}


document.addEventListener('DOMContentLoaded', async (event) => {
    // Web Workerを作成
    console.log("Worker path:", '/static/testApp/timerWorker.js');
    const timerWorker = new Worker('/static/testApp/timerWorker.js');

    // ページロード時に予約時間を取得し、それをWeb Workerに送信し、タイマーを開始する
    const urlParams = new URLSearchParams(window.location.search);
    const scheduleId = urlParams.get('scheduleId');  // URLパラメータから予約IDを取得
    if (scheduleId) {
        const { startTime, endTime } = await fetchReservationTimes(scheduleId);
        timerWorker.postMessage({ startTime, endTime });
        console.log("startTime:", startTime);
        console.log("endTime:", endTime);
        setInterval(() => updateTimerDisplay(endTime, timerWorker), 1000);
    } else {
        console.error("No scheduleId provided in the URL parameters.");
    }
});