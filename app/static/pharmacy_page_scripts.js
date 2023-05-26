const deletePharmacyButton = document.getElementById("delete-pharmacy-btn"); 
const submitButton = document.getElementById("delete-pharmacy-submit");
var deleteConfirmation = document.getElementById("delete-confirmation");
const deleteConfirmationDiv = document.getElementById("delete-confirmation-div");

deletePharmacyButton.addEventListener("click", () => {
    deleteConfirmationDiv.style.display = "block";
    submitButton.style.display = "block";
    submitButton.disabled = true;
})

deleteConfirmation.addEventListener("change", (e) => {
    const value = e.target.value;
    if (value == "delete-yes") {
        submitButton.disabled = false;
    } else if (value == "delete-no") {
        submitButton.disabled = true;
    }
})