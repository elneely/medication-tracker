const menuMedHeading = document.getElementById("menu-med-heading");
const menuMedItems = document.getElementById("menu-med-items");
const menuDoctorHeading = document.getElementById("menu-doctor-heading");
const menuDoctorItems = document.getElementById("menu-doctor-items");
const menuPharmacyHeading = document.getElementById("menu-pharmacy-heading");
const menuPharmacyItems = document.getElementById("menu-pharmacy-items");

menuMedHeading.addEventListener("click", () => {
    if (menuMedItems.style.display == "none") {
        menuMedItems.style.display = "block";
    } else {
        menuMedItems.style.display = "none";
    }
})


