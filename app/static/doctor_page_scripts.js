/* JS file for doctor.html */

/* This handles the delete confirmation section */

const deleteDoctorButton = document.getElementById("delete-doctor-btn"); 
const submitButton = document.getElementById("delete-doctor-submit");
const cancelButton = document.getElementById("cancel-delete-doctor-btn");
var deleteConfirmation = document.getElementById("delete-confirmation");
const deleteConfirmationDiv = document.getElementById("delete-confirmation-div");

deleteDoctorButton.addEventListener("click", () => {
    deleteConfirmationDiv.style.display = "block";
    submitButton.style.display = "block";
    submitButton.disabled = true;
    cancelButton.style.display = "block";
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