
document.addEventListener('DOMContentLoaded', function () {
    const swiper = new Swiper('.mySwiper', {
        loop: true,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
        pagination: {
            el: '.swiper-pagination',
            dynamicBullets: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });

    new Swiper('.categorySwiper', {
        slidesPerView: 2.5, 
        spaceBetween: 12,
        freeMode: true,     
        mousewheel: {
            forceToAxis: true, 
        },
        breakpoints: {
            340: {
                slidesPerView: 3.5,
                spaceBetween: 10
            },
            480:{
                slidesPerView: 4,
                spaceBetween: 15
            },
            640:{
                slidesPerView: 4,
                spaceBetween: 15
            },
            768: {
                slidesPerView: 5.5,
                spaceBetween: 17
            },
            1024: {
                slidesPerView: 7, 
                spaceBetween: 20,
                freeMode: true 
            }
        }
    });

    document.querySelectorAll('.wishlist-icon').forEach(icon => {
        icon.addEventListener('click', function(e) {
            e.preventDefault();
            icon.classList.toggle('active');
        });
    });
});