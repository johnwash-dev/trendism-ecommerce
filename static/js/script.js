

function get_cookie(name){
  let cookieValue = null;
  if (document.cookie && document.cookie !== ""){
    const cookies = document.cookie.split(';')
    for (let i=0; i < cookies.length;i++){
      const cookie = cookies[i].trim()

      if (cookie.substring(0, name.length + 1) === (name + '=')){
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrfToken = get_cookie('csrftoken')

async function toggleWishlist(productId, element, isWishlistPage=false){
  try{
    const response = await fetch(`/carts/toggle/${productId}/`,{
      method : 'POST',
      headers: {
        'X-CSRFToken': get_cookie('csrftoken'),
        'content-type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    })

      if (response.status === 401) {
            window.location.href = "/accounts/";
            return;
        }

        const data = await response.json();

        if (data.status === 'added') {
            element.classList.add('active');
            const icon = element.querySelector('i');
            if (icon) icon.classList.replace('fa-regular', 'fa-solid');
        } else if (data.status === 'removed' || data.status === 'remove') {
           if (isWishlistPage) {
                const rowElement = document.getElementById(`wishlist-row-${productId}`);
                if (rowElement) {
                    rowElement.classList.add('fade-out'); 
                    
                    setTimeout(() => {
                        rowElement.remove(); 
                        
                        const countSpan = document.querySelector('.wishlist-header span');
                        if(countSpan) {
                             
                        }
                    }, 500);
                }
            } else {
                element.classList.remove('active');
            }
        }
  }catch(error){
    console.error("Wishlist Error:", error);
    Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'error',
        title: 'Connection Error',
        text: 'Please check your internet or try again later.',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        iconColor: '#ff3e6c', 
    });
  }
}




let globalSelectedSizeId = null

document.addEventListener("DOMContentLoaded", function () {
  document.addEventListener('click', function (e) {
        const target = e.target.closest('.wishlist-icon, .wishlist-btn');
        if (target) {
            e.preventDefault();
            e.stopPropagation();
            const productId = target.getAttribute('data-product-id');
            if (productId) {
                toggleWishlist(productId, target);
            }
        }
    });

  const dropdownWrap = document.querySelector(".profile-dropdown");
  const menu = document.getElementById("profileDropdown");
  const icon = document.querySelector(".profile-trigger");
  let timeout;

  const alert = document.getElementById("alert-msg");

  if (dropdownWrap && menu && icon) {
        const isDesktop = window.matchMedia("(min-width: 992px)").matches;

        if (isDesktop) {
            // DESKTOP: Myntra Style Hover
            dropdownWrap.addEventListener("mouseenter", () => {
                clearTimeout(timeout);
                icon.classList.add("borders");
                menu.classList.add("show");
            });
            dropdownWrap.addEventListener("mouseleave", () => {
                timeout = setTimeout(() => {
                    icon.classList.remove("borders");
                    menu.classList.remove("show");
                }, 200);
            });
        } else {
            // MOBILE: Toggle on Click
            icon.addEventListener("click", function (e) {
                e.preventDefault();
                e.stopPropagation();
                menu.classList.toggle("show");
            });
        }

        // UNIVERSAL: Redirection handling (Works for both mobile & desktop)
        menu.addEventListener("click", function (e) {
            // Stop closing event from bubbling up to document
            e.stopPropagation();

            const target = e.target;
            const link = target.closest("a");
            const button = target.closest("button");

            if (link) {
                const url = link.getAttribute("href");
                if (url && url !== "#" && !url.startsWith("javascript")) {
                    // Direct navigation
                    window.location.href = url;
                }
            }

            if (button && button.type === "submit") {
                const form = button.closest("form");
                if (form) form.submit();
            }
        });
    }

  document.addEventListener("click", (e) => {
    if (menu && !dropdownWrap.contains(e.target)) {
      menu.classList.remove("show");
      icon.classList.remove("borders");
    }
  });

  if (alert) {
    setTimeout(function () {
      alert.classList.remove("show");
      alert.classList.add("fade");
      setTimeout(function () {
        if (alert.parentNode) {
          alert.remove();
        }
      }, 600);
    }, 5000);
  }

  window.addEventListener("load", function () {
    const preloader = document.getElementById("loader-container");
    if (preloader) {
      preloader.classList.add("loader-hidden");
      setTimeout(() => {
        preloader.remove();
      }, 500);
    }
  });

  const menuTriggers = document.querySelectorAll(".has-mega-menu");
  menuTriggers.forEach((trigger) => {
    const targetId = trigger.getAttribute("data-mega-target");
    const targetMenu = document.getElementById(targetId);

    trigger.addEventListener("mouseenter", () => {
      clearTimeout(timeout);
      document
        .querySelectorAll(".mega-menu")
        .forEach((m) => (m.style.display = "none"));

      if (targetMenu) {
        targetMenu.style.display = "block";
      }
    });

    trigger.addEventListener("mouseleave", () => {
      const body = document.body;
      timeout = setTimeout(() => {
        if (targetMenu) {
          targetMenu.style.display = "none";
          body.style.backgroundColor = "none";
        }
      }, 500);
    });
  });

  

});
