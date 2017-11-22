$(function () {

    initSwiperWheel();


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