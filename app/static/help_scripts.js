/* This contains the JS for help.html */

const helpMainSections = document.querySelectorAll(".help-heading");
const helpQuestions = document.querySelectorAll(".section-label");
const helpSubSections = document.querySelectorAll(".sub-label");

for (const section of helpMainSections) {
    section.addEventListener("click", () => {
        var relatedContainer = section.nextElementSibling;
        if (relatedContainer.style.display == "block") {
            relatedContainer.style.display = "none";
        } else {
            relatedContainer.style.display = "block";
    };
})};

for (const question of helpQuestions) {
    question.addEventListener("click", () => {
        var relatedContainer = question.nextElementSibling;
        if (relatedContainer.style.display == "block") {
            relatedContainer.style.display = "none";
        } else {
            relatedContainer.style.display = "block";
    };
})};

for (const subsection of helpSubSections) {
    subsection.addEventListener("click", () => {
        var relatedContainer = subsection.nextElementSibling;
        if (relatedContainer.style.display == "block") {
            relatedContainer.style.display = "none";
        } else {
            relatedContainer.style.display = "block";
    };
})}