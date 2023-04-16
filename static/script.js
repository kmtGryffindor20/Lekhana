
let slideIndex = 1;
var x = window.matchMedia("(max-width: 600px)")
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
showSlides(slideIndex = n);
}

function showSlides(n) {
let i;
let slides = document.getElementsByClassName("book");
if (n > slides.length) {slideIndex = 1}
if (n < 1) {slideIndex = slides.length}
for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
}
if(x.matches)
{
    slides[slideIndex-1].style.display = "flex";
    slides[slideIndex-1].style.flexDirection = "column";
}
else{
    slides[slideIndex-1].style.display = "block";
}
}


let menuBar = document.getElementsByClassName("nav-links");

menuBar[0].style.maxHeight = "0px";
function toggleMenu(){
    let menuBar = document.getElementsByClassName("nav-links");
    let image = document.getElementById("menu");
    if(menuBar[0].style.maxHeight == "250px")
    {
        menuBar[0].style.maxHeight = "0px";
        image.src = "../static/images/hamburger-icon.png";
    }
    else
    {
        menuBar[0].style.maxHeight = "250px";
        image.src = "../static/images/cross-icon.png";
    }
    
}

function fillColor(){
    let icon = document.getElementsByClassName("fav-icon");
    if (icon[0].value == "1")
    {
        icon[0].src = "../static/images/fav-no-fill.png";
        icon[0].value = "0";
    }
    else
    {
        icon[0].value = "1";
        icon[0].src = "../static/images/fav-fill.png";
    }
}
