/* JS file for add_medication.html
/* These three scripts handle the doctor portion of the form */

/*Html parts */

const doctorChoice = document.getElementById("doctor-choice");
const doctorOffers = document.getElementById("doctor-offers");
const currentDoctorDiv = document.getElementById("only-current-doctor");
var currentDoctorRadio = document.getElementById("current-doctor");
var newDoctorRadio = document.getElementById("new-doctor");
const newDoctorDiv = document.getElementById("only-new-doctor");
var doctorBtn = document.getElementById("doctor-btn");
var noDoctorBtn = document.getElementById("no-doctor-btn");
var doctorButtons = document.querySelectorAll('input[name="add-doctor"]');
var typeOfDoctor; 


/* form fields */
var currentDoctorChoice = document.getElementById("current-doctor-choice");
var newDoctorFirst = document.getElementById("new-doctor-first");
var newDoctorLast = document.getElementById("new-doctor-last");

/* Showing or hiding fields */

doctorBtn.addEventListener("click", () => {
    doctorBtn.style.display = "none";
    noDoctorBtn.style.display = "block";
    doctorChoice.style.display = "block";
    doctorOffers.style.display = "block";
    currentDoctorRadio.disabled = false;
    newDoctorRadio.disabled = false;
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
    newDoctorRadio.disabled = true;
    currentDoctorRadio.disabled = true;
}); 
doctorChoice.addEventListener("click", () => {
    for (const doctorButton of doctorButtons) {
        if (doctorButton.checked) {
            typeOfDoctor = doctorButton.value;
            sessionStorage.setItem("doctortype", doctorButton.value)
        }
    }
    if (typeOfDoctor == "current-doctor") {
        currentDoctorDiv.style.display = "block"; 
        newDoctorDiv.style.display = "none";
        newDoctorFirst.disabled = true;
        newDoctorLast.disabled = true;
        currentDoctorChoice.disabled = false;
    } else if (typeOfDoctor == "new-doctor") { 
        newDoctorDiv.style.display = "block";
        currentDoctorDiv.style.display = "none";
        currentDoctorChoice.disabled = true;
        newDoctorFirst.disabled = false;
        newDoctorLast.disabled = false;
    } 
});
/* These three scripts handle the pharmacy part of the form */

/*Html parts */

const pharmacyChoice = document.getElementById("pharmacy-choice");
const pharmacyOffers = document.getElementById("pharmacy-offers");
const currentPharmacyDiv = document.getElementById("only-current-pharmacy")
const newPharmacyDiv = document.getElementById("only-new-pharmacy")
var currentPharmacyRadio = document.getElementById("current-pharmacy");
var newPharmacyRadio = document.getElementById("new-pharmacy");
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
            sessionStorage.setItem("pharmacytype", pharmacyButton.value)
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


/* This keeps the reminder box area visible if there is an error on submit.  It
also keeps the doctor/pharmacy area visible if there is an error on submit, but only 
the first time - after that it loses the value.  Known bug.*/
document.addEventListener("DOMContentLoaded", () => {
    if (reminderAskBox.checked == true) {
        reminderTrueDiv.style.display = "block";
    }
    typeOfDoctor = sessionStorage.getItem("doctortype");
    sessionStorage.removeItem("doctortype");

    if (typeOfDoctor == "current-doctor") {
        doctorBtn.style.display = "none";
        noDoctorBtn.style.display = "block";
        currentDoctorDiv.style.display = "block"; 
        doctorChoice.style.display = "block";
        doctorOffers.style.display = "block";
        newDoctorDiv.style.display = "none";
        newDoctorFirst.disabled = true;
        newDoctorLast.disabled = true;
        currentDoctorRadio.checked = true;
    } else if (typeOfDoctor == 'new-doctor') {
        newDoctorDiv.style.display = "block";
        currentDoctorDiv.style.display = "none";
        currentDoctorChoice.disabled = true;
        doctorBtn.style.display = "none";
        noDoctorBtn.style.display = "block";
        currentDoctorDiv.style.display = "none"; 
        doctorChoice.style.display = "block";
        doctorOffers.style.display = "block";
        newDoctorRadio.checked = true;
    };

    typeOfPharmacy = sessionStorage.getItem("pharmacytype");
    sessionStorage.removeItem("pharmacytype");

    if (typeOfPharmacy == "current-pharmacy") {
        pharmacyBtn.style.display = "none";
        noPharmacyBtn.style.display = "block";
        currentPharmacyDiv.style.display = "block"; 
        pharmacyChoice.style.display = "block";
        newPharmacyDiv.style.display = "none";
        newPharmacyName.disabled = true;
        currentPharmacyRadio.checked = true;
    } else if (typeOfPharmacy == "new-pharmacy") { 
        newPharmacyDiv.style.display = "block";
        currentPharmacyDiv.style.display = "none";
        currentPharmacyChoice.value = "";

    }; 
});


