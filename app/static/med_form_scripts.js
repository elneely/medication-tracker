
/* This is to show/hide the edit medication info form */

const medicationInfoDiv = document.getElementById("edit-medication-form"); 
var editMedicationBtn = document.getElementById("edit-medication-btn");
editMedicationBtn.addEventListener("click", () => {
    if (medicationInfoDiv.style.display == "block") {
        medicationInfoDiv.style.display = "none";
    } else {
        medicationInfoDiv.style.display = "block";
    }
}); 