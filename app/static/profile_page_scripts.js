/* This holds the scripts for user_profile.html */

const deleteProfileButton = document.getElementById("delete-profile-btn"); 
const submitButton = document.getElementById("delete-profile-submit");
var deleteConfirmation = document.getElementById("delete-confirmation");
var extraConfirmation = document.getElementById("extra-confirmation");
const deleteConfirmationDiv = document.getElementById("delete-confirmation-div");
const extraConfirmationDiv = document.getElementById("extra-confirmation-div");

deleteProfileButton.addEventListener("click", () => {
    deleteConfirmationDiv.style.display = "block";
    
})

deleteConfirmation.addEventListener("change", (e) => {
    const value = e.target.value;
    if (value == "delete-yes") {
        extraConfirmationDiv.style.display = "block";
        submitButton.style.display = "block";
        submitButton.disabled = true;

    } else if (value == "delete-no") {
        extraConfirmationDiv.style.display = "none";
        submitButton.style.display = "none";
        submitButton.disabled = true;
    }
})

extraConfirmation.addEventListener("change", (e) => {
    const value = e.target.value;
    if (value == "certain-yes") {
        submitButton.disabled = false;
    } else if (value == "certain-no") {
        submitButton.disabled = true;
    }
})