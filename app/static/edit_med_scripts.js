
/* This script handles the reminder box */
var reminderAskBox = document.getElementById("reminders-ask");
const reminderTrueDiv = document.getElementById("reminders-true");
reminderAskBox.addEventListener("click", () => {
    if (reminderAskBox.checked == true) {
        reminderTrueDiv.style.display = "block";
    }
    else {
        reminderTrueDiv.style.display = "none";
    }
    });

document.addEventListener("DOMContentLoaded", () => {
    if (reminderAskBox.checked == true) {
        reminderTrueDiv.style.display = "block";
    }
});