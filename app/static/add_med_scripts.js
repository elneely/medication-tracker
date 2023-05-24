/* These three scripts handle the doctor portion of the form */

/*Html parts */

const doctorChoice = document.getElementById("doctor-choice");
const doctorOffers = document.getElementById("doctor-offers");
const currentDoctorDiv = document.getElementById("only-current-doctor")
const newDoctorDiv = document.getElementById("only-new-doctor")
var doctorBtn = document.getElementById("doctor-btn");
var noDoctorBtn = document.getElementById("no-doctor-btn");
var doctorButtons = document.querySelectorAll('input[name="add-doctor"]');
var typeOfDoctor; 

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
/* These three scripts handle the pharmacy part of the form */

/*Html parts */

const pharmacyChoice = document.getElementById("pharmacy-choice");
const pharmacyOffers = document.getElementById("pharmacy-offers");
const currentPharmacyDiv = document.getElementById("only-current-pharmacy")
const newPharmacyDiv = document.getElementById("only-new-pharmacy")
var pharmacyBtn = document.getElementById("pharmacy-btn");
var noPharmacyBtn = document.getElementById("no-pharmacy-btn");
var pharmacyButtons = document.querySelectorAll('input[name="add-pharmacy"]');
var typeOfPharmacy; 

/* form fields */
var currentPharmacyChoice = document.getElementById("current-pharmacy-choice");
var newPharmacyName = document.getElementById("new-pharmacy-name");


pharmacyBtn.addEventListener("click", () => {
    pharmacyBtn.style.display = "none";
    noPharmacyBtn.style.display = "block";
    pharmacyChoice.style.display = "block";
    pharmacyOffers.style.display = "block";
    newPharmacyName.disabled = false;
    currentPharmacyChoice.disabled = false;
}); 

noPharmacyBtn.addEventListener("click", () => {
    noPharmacyBtn.style.display = "none";
    pharmacyBtn.style.display = "block";
    pharmacyOffers.style.display = "none";
    pharmacyChoice.style.display = "none";
    currentPharmacyChoice.disabled = true;
    newPharmacyName.disabled = true;
});

pharmacyChoice.addEventListener("click", () => {
    for (const pharmacyButton of pharmacyButtons) {
        if (pharmacyButton.checked) {
            typeOfPharmacy = pharmacyButton.value;
        }
    }
    if (typeOfPharmacy == "current-pharmacy") {
        currentPharmacyDiv.style.display = "block"; 
        newPharmacyDiv.style.display = "none";
        newPharmacyName.value = "";
    } else if (typeOfPharmacy == "new-pharmacy") { 
        newPharmacyDiv.style.display = "block";
        currentPharmacyDiv.style.display = "none";
        currentPharmacyChoice.value = "";

    } 
}); 

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