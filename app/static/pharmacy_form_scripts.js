/* This is to show/hide the edit doctor info form */

const pharmacyInfoDiv = document.getElementById("edit-pharmacy-form"); 
var editPharmacyBtn = document.getElementById("edit-pharmacy-btn");
editPharmacyBtn.addEventListener("click", () => {
    if (pharmacyInfoDiv.style.display == "block") {
        pharmacyInfoDiv.style.display = "none";
    } else {
        pharmacyInfoDiv.style.display = "block";
    }
}); 