// Custom
// Active tab in sidebar
var tabs = document.querySelectorAll('.navbar-sidebar .navbar__list li');

var pathName = window.location.pathname;
var activeTab = pathName.substring(pathName.lastIndexOf('/') + 1);

console.log(activeTab);

tabs[0].classList.add("active")

for (var i = 0; i < tabs.length; i++) {
    if (tabs[i].getAttribute('data-tab') === activeTab) {
        tabs[i].classList.add('active');
    } else {
        tabs[i].classList.remove('active');
    }
}

// Color is changed by spam percent
var spamPercentCard = document.querySelector(".overview-item--c1");
if (spamPercentCard) {
    var spamPercent = Number(spamPercentCard.getAttribute("data-spam"));

    if (spamPercent >= 30 && spamPercent <= 60) {
        spamPercentCard.style.backgroundImage = "-webkit-linear-gradient(90deg, #fffc66 0%, #c4c106 100%)";
    } else if (spamPercent > 60) {
        spamPercentCard.style.backgroundImage = "-webkit-linear-gradient(90deg, #ff8080 0%, #ff1212 100%)";
    } else {
        spamPercentCard.style.backgroundImage = "-webkit-linear-gradient(90deg, #7aafff 0%, #0040ff 100%)";
    }
}
