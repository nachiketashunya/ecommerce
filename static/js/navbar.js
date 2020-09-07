//get user section btn
const userSectionBtn = document.querySelector(".user-icon");
//get user section 
const userSection = document.querySelector(".user-section");

const hambergerSection = document.querySelector(".hamberger-section");
const hambergerBtn = document.querySelector(".hamberger-icon");

// event listener to user section button 
userSectionBtn.addEventListener("click", showUserSection);

function showUserSection() {
    hambergerSection.classList.remove("show-hamberger-content");

    userSection.classList.toggle("show-user-section");
}


// event listener to hamberger section 
hambergerBtn.addEventListener("click", showHambergerContent);

function showHambergerContent() {
    userSection.classList.remove("show-user-section");

    hambergerSection.classList.toggle("show-hamberger-content");
}
