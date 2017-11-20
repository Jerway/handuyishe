$(function () {

    initSwiperWheel();

    li_omit = $('#li_omit');
    a_pagination = $('#ul_pagination_bottom a');
    li_total = $('#li_total')[0].innerHTML.substr(1,2);
    console.log(li_total);
    li_omit.click(function () {

        console.log('i do');
        console.log(a_pagination.length, parseInt(li_total));
        for (var i = 0; i < a_pagination.length; i++) {

            if (parseInt(a_pagination[i].innerHTML) < parseInt(li_total)) {
                a_pagination[i].innerHTML = parseInt(a_pagination[i].innerHTML) + 8;
            }
            if (parseInt(a_pagination[i].innerHTML) === parseInt(li_total)){
                console.log(a_pagination.indexOf(a_pagination[i]));
            }
        }

    })


});

function initSwiperWheel() {

    var swiper = new Swiper('.swiper-container', {
        effect: 'cube',
        grabCursor: true,
        autoplay: 3000,
        cube: {
            shadow: true,
            slideShadows: true,
            shadowOffset: 20,
            shadowScale: 0.94
        }
    });
}