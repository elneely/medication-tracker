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
