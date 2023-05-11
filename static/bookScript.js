let currentTab = 0;
openTab(0);

function openTab(n)
{
    let i;
    let cards = document.querySelectorAll(".tab-data");
    console.log(cards.length);
    for(i = 0; i < 3; i++)
    {
        cards[i].style.display = 'none';
    }
    let page = ""+n;
    cards[page].style.display = 'block';
    if (n == 2) {
        cards[page].style.display = 'flex';   
    }

    let tabs = document.querySelectorAll('.tab');
    for(i = 0; i < tabs.length; i++)
    {
        let classes = tabs[i].classList;
        if (classes.contains('active')) {
            
            classes.remove('active');
        }
        if(i == n)
        {
            classes.add('active');
        }
    }
    
}