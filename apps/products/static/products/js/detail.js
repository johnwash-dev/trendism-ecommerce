document.addEventListener('DOMContentLoaded', function() {

    if (document.querySelector('.mobile-swiper')) {
        new Swiper('.mobile-swiper', {
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            loop: true,
        });
    }

    if (document.querySelector('.similar-swiper')) {
        new Swiper('.similar-swiper', {
            slidesPerView: 2.2, 
            spaceBetween: 10,
            pagination: {
                el: '.similar-swiper .swiper-pagination',
                clickable: true,
            },
            loop: false,
        });
    }

    const mainImg = document.getElementById('mainImg');
    const colorSwatches = document.querySelectorAll('.swatch-wrapper[data-variant-img]');
    
    if (mainImg) {
        const originalSrc = mainImg.src;

        colorSwatches.forEach(swatch => {
            swatch.addEventListener('mouseenter', function() {
                const newSrc = this.getAttribute('data-variant-img');
                
                // Add fade out effect
                mainImg.classList.add('img-fade-out');
                
                setTimeout(() => {
                    mainImg.src = newSrc;
                    mainImg.classList.remove('img-fade-out');
                }, 150);
            });

            swatch.addEventListener('mouseleave', function() {
                mainImg.classList.add('img-fade-out');
                
                setTimeout(() => {
                    mainImg.src = originalSrc;
                    mainImg.classList.remove('img-fade-out');
                }, 150);
            });
        });
    }

    document.querySelectorAll("#size-btns").forEach(size =>{
        size.addEventListener('click', ()=>{
            document.querySelectorAll(".size-btn").forEach(btns =>{
                btns.classList.remove("btn-active")
            })
            size.classList.add("btn-active")
        })
    })
});

function changeImage(src, element) {
    const mainImg = document.getElementById('mainImg');
    if (mainImg) {
        mainImg.src = src;
        document.querySelectorAll('.thumb-item').forEach(img => {
            img.classList.remove('thumb-active');
        });

        element.classList.add('thumb-active');
    }
}