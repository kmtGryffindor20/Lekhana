let pageIndex = 0;
Page(pageIndex);

function nextPage(n) {
    Page(pageIndex += n);
    
}

function prevPage(n) {
    Page(pageIndex += n);
}

function Page(n){
    let i;
    let pages = document.getElementsByClassName("page");
    if (n >= pages.length/10)
    {
        pageIndex = 0;
    }
    else if ( n < 0)
    {
        pageIndex = pages.length/10 - 1;
    }
    else{
        pageIndex = n;
    }
    let page = "page"+(pageIndex);
    let pageN = document.getElementsByClassName(page);
    for (i = 0; i < pages.length; i++)
    {
        pages[i].style.display = "none";
    }

    for (i = 0; i < pageN.length; i++)
    {
        pageN[i].style.display = "block";
    }

    let indexes = document.querySelectorAll('.number')
    for(i = 0; i < indexes.length; i++)
    {
        let classes = indexes[i].classList;
        if(classes.contains('active'))
        {
            classes.remove('active');
        }
        indexes[i].style.display = 'none';
    }
    indexes[indexes.length - 1].style.display = 'block';
    if (pageIndex == 0 || pageIndex == 1)
    {
        indexes[1].style.display = 'block';
        indexes[2].style.display = 'block';
        indexes[3].style.display = 'block';
    }
    else if (pageIndex >= pages.length/10 - 1)
    {
        indexes[0].style.display = 'block';
        indexes[pageIndex-1].style.display = 'block';
        indexes[pageIndex].style.display = 'block';
        indexes[pageIndex + 1].style.display = 'block';
        indexes[indexes.length - 1].style.display = 'none';
    }
    else
    {
        indexes[0].style.display = 'block';
        indexes[pageIndex].style.display = 'block';
        indexes[pageIndex + 2].style.display = 'block';
        indexes[pageIndex + 1].style.display = 'block';
    }
    indexes[pageIndex+1].classList.add('active');
}