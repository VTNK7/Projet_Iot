// Enable Notifications Button
const enableButton = document.getElementById('enable-notifications');

// Event listener to enable browser notifications
enableButton.addEventListener('click', () => {
    if ("Notification" in window) {
        if (Notification.permission === "default") {
            Notification.requestPermission().then(permission => {
                if (permission === "granted") {
                    alert("Notifications activées !");
                } else {
                    alert("Vous devez autoriser les notifications.");
                }
            });
        } else if (Notification.permission === "granted") {
            alert("Les notifications sont déjà activées !");
        } else {
            alert("Vous avez refusé les notifications. Modifiez les paramètres de votre navigateur pour les activer.");
        }
    } else {
        alert("Votre navigateur ne supporte pas les notifications.");
    }
});

// Connect to the Flask-SocketIO server
const socket = io();

// Listen for the 'notification' event
socket.on('notification', function(data) {
    // Check if notifications are granted
    if (Notification.permission === "granted") {
        new Notification("Nouvelle Notification", {
            body: data.message, // The message received from the server
            icon: "https://cdn-icons-png.flaticon.com/512/847/847969.png" // Optional: Add a notification icon
        });
    } else {
        console.log("Les notifications ne sont pas activées. Message : ", data.message);
    }
});