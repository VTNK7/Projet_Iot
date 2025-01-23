self.addEventListener("push", function (event) {
    const data = event.data.text();
    self.registration.showNotification("Push Notification", {
        body: data,
        icon: "/static/icon.png",
    });
});