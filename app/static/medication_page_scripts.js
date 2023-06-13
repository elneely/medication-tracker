/* This holds the JS for medication.html */

const deleteMedicationButton = document.getElementById("delete-medication-btn"); 
const submitButton = document.getElementById("delete-medication-submit");
const cancelButton = document.getElementById("cancel-delete-medication-btn");
var deleteConfirmation = document.getElementById("delete-confirmation");
const deleteConfirmationDiv = document.getElementById("delete-confirmation-div");

deleteMedicationButton.addEventListener("click", () => {
    deleteConfirmationDiv.style.display = "block";
    submitButton.style.display = "block";
    submitButton.disabled = true;
    cancelButton.style.display = "block";
    deleteMedicationButton.style.display = "none";
});

deleteConfirmation.addEventListener("change", (e) => {
    const value = e.target.value;
    if (value == "delete-yes") {
        submitButton.disabled = false;
    } else if (value == "delete-no") {
        submitButton.disabled = true;
    }
});
cancelButton.addEventListener("click", () => {
    location.replace(location.href);
}
);