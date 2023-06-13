/* This holds the JS for pharmacy.html */

const deletePharmacyButton = document.getElementById("delete-pharmacy-btn"); 
const submitButton = document.getElementById("delete-pharmacy-submit");
const cancelButton = document.getElementById("cancel-delete-pharmacy-btn");
var deleteConfirmation = document.getElementById("delete-confirmation");
const deleteConfirmationDiv = document.getElementById("delete-confirmation-div");

deletePharmacyButton.addEventListener("click", () => {
    deleteConfirmationDiv.style.display = "block";
    submitButton.style.display = "block";
    submitButton.disabled = true;
    cancelButton.style.display = "block";
    deletePharmacyButton.style.display = "none";
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