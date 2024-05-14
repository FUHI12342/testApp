self.onmessage = function(event) {
    const now = event.data;
    console.log("event.data:", event.data);  // event.dataをログに出力
    const endTime = new Date(event.data);
    console.log("endTime:", endTime);
    setInterval(() => {
        const currentTime = new Date();
        const remainingTime = endTime - currentTime;
        // 残り時間をメインスレッドに送信
        self.postMessage(remainingTime);
    }, 1000);
};