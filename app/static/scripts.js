
const targetDiv = document.getElementById("doctor-choice");
const targetMessage = document.getElementById("doctor-offers");
var doctorBtn = document.getElementById("doctor-btn");
doctorBtn.addEventListener("click", () => {
    if (targetDiv.style.display == "block") {
        targetDiv.style.display = "none";
        targetMessage.style.display = "none";
    } else {
        targetDiv.style.display = "block";
        targetMessage.style.display = "block";
        if (document.getElementById("new-doctor").checked) {
            document.querySelector('#new-doctor').click();
        } else {
            document.querySelector('#current-doctor').click();
        }
    }
}); 

var doctorButtons = document.querySelectorAll('input[name="add-doctor"]');
var typeOfDoctor;
const currentDoctorDiv = document.getElementById("only-current-doctor")
const newDoctorDiv = document.getElementById("only-new-doctor")
targetDiv.addEventListener("click", () => {
    for (const doctorButton of doctorButtons) {
        if (doctorButton.checked) {
            typeOfDoctor = doctorButton.value;
        }
    }
    if (typeOfDoctor == "current-doctor") {
        currentDoctorDiv.style.display = "block";
        newDoctorDiv.style.display = "none";
    } else if (typeOfDoctor == "new-doctor") {
        newDoctorDiv.style.display = "block";
        currentDoctorDiv.style.display = "none";
    } 
});


var reminderAskBox = document.getElementById("reminders-ask");
const reminderTrueDiv = document.getElementById("reminders-true");
reminderAskBox.addEventListener("click", () => {
    if (reminderAskBox.checked == true){
        reminderTrueDiv.style.display = "block";
    }
    else {
        reminderTrueDiv.style.display = "none";
    }
    });

 
    