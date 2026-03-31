function get_cookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();

      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrfToken = get_cookie("csrftoken");

async function toggleWishlist(productId, element, isWishlistPage = false) {
  try {
    const response = await fetch(`/carts/toggle/${productId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": get_cookie("csrftoken"),
        "content-type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
    });

    if (response.status === 401) {
      window.location.href = "/accounts/";
      return;
    }

    const data = await response.json();

    if (data.status === "added") {
      element.classList.add("active");
      const icon = element.querySelector("i");
      if (icon) icon.classList.replace("fa-regular", "fa-solid");
    } else if (data.status === "removed" || data.status === "remove") {
      if (isWishlistPage) {
        const rowElement = document.getElementById(`wishlist-row-${productId}`);
        if (rowElement) {
          rowElement.classList.add("fade-out");

          setTimeout(() => {
            rowElement.remove();

            const countSpan = document.getElementById("wishlist-count");
            if (countSpan && data.wishlist_count !== undefined) {
              countSpan.innerText = `(${data.wishlist_count} Items)`;
            }

            // Check if wishlist is now empty and show empty message
            if (data.wishlist_count === 0) {
              const rowContainer = document.querySelector(".wishlist-row");
              if (rowContainer) {
                const emptyMessage = document.createElement("div");
                emptyMessage.className = "col-12 text-center py-5";
                emptyMessage.innerHTML = `
                  <p class="text-muted">Your wishlist is empty!</p>
                  <a href="/products/" class="btn btn-pink px-4 py-2">Continue Shopping</a>
                `;
                rowContainer.appendChild(emptyMessage);
              }
            }
          }, 500);
        }
      } else {
        element.classList.remove("active");
      }
    }
  } catch (error) {
    Swal.fire({
      toast: true,
      position: "top-end",
      icon: "error",
      title: "Connection Error",
      text: "Please check your internet or try again later.",
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true,
      iconColor: "#ff3e6c",
    });
  }
}

let globalSelectedSizeId = null;

function selectProductSize(element, sizeId, containerId) {
  globalSelectedSizeId = sizeId;

  const container = document.getElementById(containerId);

  if (container) {
    container.querySelectorAll("button").forEach((btn) => {
      btn.classList.remove("btn-active", "active-size");
    });

    if (element.classList.contains("home-size-btn")) {
      element.classList.add("active-size");
    } else {
      element.classList.add("btn-active");
    }
    container.classList.remove("shake-container");
  }
}

async function add_to_cart(productId, isModal = false) {
  const containerId = isModal
    ? `size-container-${productId}`
    : `size-btns-container`;
  const container = document.getElementById(containerId);

  if (!globalSelectedSizeId) {
    if (container) {
      container.classList.add("shake-container");
      setTimeout(() => container.classList.remove("shake-container"), 400);
    }
    return;
  }

  if (isModal) {
        const modalId = `quickSizeModal${productId}`;
        const modalElement = document.getElementById(modalId);
        if (modalElement) {
          const modalInstance = bootstrap.Modal.getInstance(modalElement);
          if (modalInstance) {
            modalInstance.hide();
          }
        }
      };

  try {
    const response = await fetch("/carts/add/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": get_cookie("csrftoken"),
        "X-Requested-With": "XMLHttpRequest",
      },
      body: JSON.stringify({
        product_id: productId,
        size_id: globalSelectedSizeId,
      }),
    });

    const data = await response.json();

    if (response.status === 401) {
      window.location.href = "/accounts/";
      return;
    }

    if (data.status === "success") {
      

      const cartCounterBadge = document.querySelector(".cart-counter");
      if (cartCounterBadge) {
        cartCounterBadge.innerText = data.cart_count;
        cartCounterBadge.classList.add("badge-pop");
        setTimeout(() => cartCounterBadge.classList.remove("badge-pop"), 300);
      }

      Swal.fire({
        toast: true,
        position: "top-end",
        icon: "success",
        title: data.message,
        showConfirmButton: false,
        timer: 2000,
        background: "#282c3f",
        color: "#fff",
      });

      globalSelectedSizeId = null;
    } else {
      Swal.fire({ icon: "error", title: "Oops...", text: data.message });
    }
  } catch (error) {
    Swal.fire({
      toast: true,
      position: "top-end",
      icon: "error",
      title: "Connection Error",
      text: "Please check your internet or try again later.",
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true,
      iconColor: "#ff3e6c",
    });
  }
}

async function updateQuantity(itemId, action) {
  const url = `/carts/update/${itemId}/${action}/`;

  try {
    const response = await fetch(url, {
      method: "GET",
      headers: { "X-Requested-With": "XMLHttpRequest" },
    });
    
    const data = await response.json();

    if (data.status === "success") {
      document.getElementById(`qty-${itemId}`).innerText = data.quantity;
      document.getElementById(`subtotal-${itemId}`).innerText = data.sub_total;

      const origPriceElem = document.getElementById(`orig-price-${itemId}`);
      if (origPriceElem) {
        origPriceElem.innerText = `₹${data.original_price_total}`;
      }

      const discountPercentElem = document.getElementById(
        `discount-percent-${itemId}`,
      );
      if (discountPercentElem && data.original_price_total > 0) {
        const off =
          ((data.original_price_total - data.sub_total) /
            data.original_price_total) *
          100;
        discountPercentElem.innerText = `${Math.round(off)}% OFF`;
      }

      const cartCounter = document.querySelector(".cart-counter");

      if (cartCounter) cartCounter.innerText = data.cart_count;

    } else if (data.status === "removed") {
      const row = document.getElementById(`item-row-${itemId}`);
      if (row) row.remove();
      if (data.cart_count === 0) {
        location.reload();
        return;
      }
    }

    document.getElementById("total-mrp").innerText = `₹${data.total_mrp}`;
    document.getElementById("total-discount").innerText = `-₹${data.total_discount}`;
    document.getElementById("final-total").innerText = `₹${data.cart_total}`;

    const navCartCount = document.getElementById("cart-count");
    if (navCartCount && data.cart_count !== undefined) {
      navCartCount.innerText = data.cart_count;
    }
  } catch (error) {
    Swal.fire({
      toast: true,
      position: "top-end",
      icon: "error",
      title: "Connection Error",
      text: "Please check your internet or try again later.",
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true,
      iconColor: "#ff3e6c",
    });
  }
}

async function removeItem(itemId) {
  const bagCountElem = document.getElementById("bag-count");
  const row = document.getElementById(`item-row-${itemId}`);

  if (row) {
        row.style.opacity = '0.5'; 
    }

  try {
    const response = await fetch(`/carts/remove/${itemId}/`, {
      headers: { "X-Requested-With": "XMLHttpRequest" },
    });
    const data = await response.json();

    if (data.status === "removed") {
      if (row) row.remove();

      if (data.cart_count === 0) {
        location.reload();
      } else {
        document.getElementById("total-mrp").innerText = `₹${data.total_mrp}`;
        document.getElementById("total-discount").innerText =
          `-₹${data.total_discount}`;
        document.getElementById("final-total").innerText =
          `₹${data.cart_total}`;
      }
      if (bagCountElem) bagCountElem.innerText = data.cart_count;

      const navCartCount = document.querySelector(".cart-counter");
      if (navCartCount) navCartCount.innerText = data.cart_count;
    }
  } catch (error) {
    Swal.fire({
      toast: true,
      position: "top-end",
      icon: "error",
      title: "Connection Error",
      text: "Please check your internet or try again later.",
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true,
      iconColor: "#ff3e6c",
    });
  }
}

document.addEventListener("DOMContentLoaded", function () {
  document.addEventListener("click", function (e) {
    const target = e.target.closest(".wishlist-icon, .wishlist-btn");
    if (target) {
      e.preventDefault();
      e.stopPropagation();
      const productId = target.getAttribute("data-product-id");
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
