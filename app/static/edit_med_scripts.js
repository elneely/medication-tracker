/* This JS file holds the scripts for edit_medication.html */

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

/* This keeps the reminder area visible if there is an error on submit */
document.addEventListener("DOMContentLoaded", () => {
    if (reminderAskBox.checked == true) {
        reminderTrueDiv.style.display = "block";
    }
});