/* This is going to handle the check all box */

var checkAllBox = document.getElementById("all-medications");
var singleCheckbox = document.getElementsByClassName("selected_medications");

checkAllBox.addEventListener("click", () => {
    if (checkAllBox.checked == false) {
        for (const box of singleCheckbox) {
            if (box.checked == true) {
                box.checked = false;
        }
    }
    } else if (checkAllBox.checked == true) {
        for (const box of singleCheckbox) {
            if (box.checked == false) {
                box.checked = true;
        }
    }
    }
});


/* Action choice portion */
const doctorSection = document.getElementById("doctors-list");
const pharmacySection = document.getElementById("pharmacy-list");
const submitButton = document.getElementById("manage-meds-submit-button");
const deleteConfirmation = document.getElementById("delete-confirmation");
const actionChoice = document.getElementById("action-choice"); 

actionChoice.addEventListener("change", (e) => {
    const value = e.target.value;
    if (value == "change-doctor") {
        doctorSection.style.display = "block";
        submitButton.style.display = "block";
        pharmacySection.style.display = "none";
        deleteConfirmation.style.display = "none";
    } else if (value == "change-pharmacy") {
        pharmacySection.style.display = "block";
        submitButton.style.display = "block";
        doctorSection.style.display = "none";
        deleteConfirmation.style.display = "none";
    } else if (value == "delete-medication") {
        deleteConfirmation.style.display = "block";
        submitButton.style.display = "block";
        doctorSection.style.display = "none";
        pharmacySection.style.display = "none";
    } else {
        doctorSection.style.display = "none";
        pharmacySection.style.display = "none";
        deleteConfirmation.style.display = "none";
        submitButton.style.display = "none";
    }
});

/* No action selected portion */

/* Edit Doctor portion */

 


/* Edit Pharmacy portion */

/* Delete medication portion */