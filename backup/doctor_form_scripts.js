/* This is to show/hide the edit doctor info form */

const doctorInfoDiv = document.getElementById("edit-doctor-form"); 
var editDoctorBtn = document.getElementById("edit-doctor-btn");
editDoctorBtn.addEventListener("click", () => {
    if (doctorInfoDiv.style.display == "block") {
        doctorInfoDiv.style.display = "none";
    } else {
        doctorInfoDiv.style.display = "block";
    }
}); 