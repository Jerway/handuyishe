$(function () {

    initSwiperWheel();


});

function initSwiperWheel() {

    var swiper = new Swiper('.swiper-container', {
        effect: 'coverflow',
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: 'auto',
        coverflow: {
            rotate: 20,
            stretch: 3,
            depth: 20,
            modifier: 3,
            slideShadows : true
        }
    });

}