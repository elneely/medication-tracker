/* This governs what happens when the Add Doctor button is pressed - it 
hides this button, makes the No doctor button visible, checks to see if 
a radio button is checked and, if so, handles it appropriately.  It defaults
to current doctor */

/*Html parts */

const doctorChoice = document.getElementById("doctor-choice");
const doctorOffers = document.getElementById("doctor-offers");
const currentDoctorDiv = document.getElementById("only-current-doctor")
const newDoctorDiv = document.getElementById("only-new-doctor")
var doctorBtn = document.getElementById("doctor-btn");
var noDoctorBtn = document.getElementById("no-doctor-btn");
var doctorButtons = document.querySelectorAll('input[name="add-doctor"]');
var typeOfDoctor
var form = document.getElementById("med-form")

/* form fields */
var currentDoctorChoice = document.getElementById("current-doctor-choice");
var newDoctorFirst = document.getElementById("new-doctor-first");
var newDoctorLast = document.getElementById("new-doctor-last");

doctorBtn.addEventListener("click", () => {
    doctorBtn.style.display = "none";
    noDoctorBtn.style.display = "block";
    doctorChoice.style.display = "block";
    doctorOffers.style.display = "block";
    newDoctorFirst.disabled = false;
    newDoctorLast.disabled = false;
    currentDoctorChoice.disabled = false;
    if (document.getElementById("new-doctor").checked) {
        document.querySelector('#new-doctor').click();
    } else {
        document.querySelector('#current-doctor').click();
    }

}) 

noDoctorBtn.addEventListener("click", () => {
    noDoctorBtn.style.display = "none";
    doctorBtn.style.display = "block";
    currentDoctorChoice.disabled = true;
    newDoctorFirst.disabled = true;
    newDoctorLast.disabled = true;
    doctorOffers.style.display = "none";
    doctorChoice.style.display = "none";
});



doctorChoice.addEventListener("click", () => {
    for (const doctorButton of doctorButtons) {
        if (doctorButton.checked) {
            typeOfDoctor = doctorButton.value;
        }
    }
    if (typeOfDoctor == "current-doctor") {
        currentDoctorDiv.style.display = "block"; 
        newDoctorDiv.style.display = "none";
        newDoctorFirst.value = "";
        newDoctorLast.value = "";
    } else if (typeOfDoctor == "new-doctor") { 
        newDoctorDiv.style.display = "block";
        currentDoctorDiv.style.display = "none";
        currentDoctorChoice.value = "";

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
 
