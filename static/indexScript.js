let slideIndex = 1;
(function(){
    let body = document.getElementsByTagName('body')[0];
    let currentTheme = body.getAttribute('data-bs-theme');
    console.log(currentTheme);
    let targetTheme = localStorage.getItem('theme');
    console.log(targetTheme);

    if(currentTheme != targetTheme)
        changeTheme();
})();
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
    slides[slideIndex-1].style.display = "block";
}




function changeTheme() {

    let i;
    let body = document.getElementsByTagName('body')[0];
    let texts = document.getElementsByClassName("text");
    let btn = document.getElementsByClassName('btn');
    let border = document.getElementsByClassName('border');
    let blueBlack = document.getElementsByClassName('X');
    let themeButton = document.getElementsByClassName('bi')[0];


    var root = document.querySelector(':root');


    themeButton.classList.toggle('bi-brightness-high');
    themeButton.classList.toggle('bi-moon');

    let path = document.getElementsByTagName('path')[0];
    let image = document.getElementsByClassName('signup-img')[0];
    let theme = body.getAttribute('data-bs-theme');
    if(theme == 'dark')
    {
        body.setAttribute('data-bs-theme', 'primary');
        path.setAttribute('d', "M6 .278a.768.768 0 0 1 .08.858 7.208 7.208 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277.527 0 1.04-.055 1.533-.16a.787.787 0 0 1 .81.316.733.733 0 0 1-.031.893A8.349 8.349 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.752.752 0 0 1 6 .278zM4.858 1.311A7.269 7.269 0 0 0 1.025 7.71c0 4.02 3.279 7.276 7.319 7.276a7.316 7.316 0 0 0 5.205-2.162c-.337.042-.68.063-1.029.063-4.61 0-8.343-3.714-8.343-8.29 0-1.167.242-2.278.681-3.286z");

        root.style.setProperty("--text-color","#17a2b8");
        root.style.setProperty("--text-bg","#17a2b8b4"); 
        root.style.setProperty("--bg-image", "url(../static/images/bg-image-light.jpg)");
        if(image != null)
        image.setAttribute('src', "../static/images/draw1.webp");
        root.style.setProperty('--signup-pic', "../static/images/draw1.webp");
        localStorage.setItem('theme', 'light');
    }
    else
    {
        body.setAttribute('data-bs-theme', 'dark');
        path.setAttribute('d', 'M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z');
        root.style.setProperty("--text-color","#ffc107");
        root.style.setProperty("--text-bg","#ffc107b4");
        root.style.setProperty("--bg-image","url(../static/images/bg-image_.jpg)");
        if(image != null)
        image.setAttribute('src', "../static/images/draw1-dark.jpg");

        root.style.setProperty('--signup-pic', "../static/images/draw1-dark.jpg");

        localStorage.setItem('theme', 'dark');
    }

    for(i = 0; i < blueBlack.length; i++)
    {
        blueBlack[i].classList.toggle('bg-dark');
        blueBlack[i].classList.toggle('bg-light');
    }
    


    for(i = 0; i < texts.length; i++)
    {
        let classes = texts[i].classList;
        classes.toggle('text-warning');
        classes.toggle('text-info');

    }

    for(i = 0; i < btn.length; i++)
    {
        btn[i].classList.toggle('btn-outline-warning');
        btn[i].classList.toggle('btn-outline-info');
    }

    for (i = 0; i < border.length; i++)
    {
        border[i].classList.toggle('border-warning');
        border[i].classList.toggle('border-info');
    }
}



