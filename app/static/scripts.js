var newDoctorFlag  

/*This listens to the add doctor button so that if it is pressed it will toggle
the visibility of the radio buttons for new/current doctor choice */

const doctorChoice = document.getElementById("doctor-choice");
const doctorOffers = document.getElementById("doctor-offers");
var doctorBtn = document.getElementById("doctor-btn");
var currentDoctorChoice = document.getElementById("current-doctor-choice");
var newDoctorFirst = document.getElementById("new-doctor-first");
var newDoctorLast = document.getElementById("new-doctor-last");
doctorBtn.addEventListener("click", () => {
    if (doctorChoice.style.display == "block") {
        doctorChoice.style.display = "none";
        doctorOffers.style.display = "none";
        currentDoctorChoice.disabled = true;
        newDoctorFirst.disabled = true;
        newDoctorLast.disabled = true;
    } else {
        doctorChoice.style.display = "block";
        doctorOffers.style.display = "block";
        currentDoctorChoice.disabled = false;
        newDoctorFirst.disabled = false;
        newDoctorLast.disabled = false;
        if (newDoctorFlag == true) {
            document.querySelector('#new-doctor').click();
        } else {
            document.querySelector('#current-doctor').click();
        }
    }
}); 

/*This governs the input of the radio buttons so that the correct part
of the form displays depending on whether you are entering a new or 
current doctor */

var doctorButtons = document.querySelectorAll('input[name="add-doctor"]');
const currentDoctorDiv = document.getElementById("only-current-doctor")
const newDoctorDiv = document.getElementById("only-new-doctor")
doctorChoice.addEventListener("click", () => {
    for (const doctorButton of doctorButtons) {
        if (doctorButton.checked) {
            typeOfDoctor = doctorButton.value;
        }
    }
    if (typeOfDoctor == "current-doctor") {
        newDoctorFlag = false;
        currentDoctorDiv.style.display = "block"; 
        currentDoctorChoice.disabled = false;
        newDoctorDiv.style.display = "none";
        newDoctorFirst.disabled = true;
        newDoctorLast.disabled = true;
    } else if (typeOfDoctor == "new-doctor") {
        newDoctorFlag = true;
        newDoctorDiv.style.display = "block";
        newDoctorFirst.disabled = false;
        newDoctorLast.disabled = false;
        currentDoctorDiv.style.display = "none";
        currentDoctorChoice.disabled = true;
    } 
});

/* This looks to see if refill reminders are requested and, if so, displays
the part of the form that asks how far in advance you want them */

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

 
    