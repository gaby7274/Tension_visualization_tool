self.addEventListener('message', function(e) {
    console.log("SIIII PAAA");
    self.postMessage({worker_id:1})
}, false);
