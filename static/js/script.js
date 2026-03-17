document.addEventListener("DOMContentLoaded", function () {
  const dropdownWrap = document.querySelector(".profile-dropdown");
  const menu = document.getElementById("profileDropdown");
  const icon = document.querySelector(".profile-trigger");
  let timeout;

  const alert = document.getElementById("alert-msg");

  if (dropdownWrap && menu && icon) {
    const isDesktop = window.matchMedia("(min-width: 992px)").matches;

    if (isDesktop) {
      // DESKTOP: Hover logic
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
      // MOBILE: Toggle logic with Flag to prevent double trigger
      let isToggling = false;
      const handleToggle = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (isToggling) return;
        isToggling = true;
        menu.classList.toggle("show");
        setTimeout(() => {
          isToggling = false;
        }, 300); // 300ms cooldown
      };

      // Use only click for mobile/desktop-responsive compatibility
      // Mobile browsers usually simulate click 300ms after touch
      icon.addEventListener("click", handleToggle);

      // Menu content handling - Professional Delegation
      menu.addEventListener("click", function (e) {
        // Step 1: Bootstrap global close-ah stop panrom
        e.stopPropagation();

        const target = e.target;
        const link = target.closest("a");
        const button = target.closest("button");

        // CASE A: Links (Login, Profile etc.)
        if (link) {
          const url = link.getAttribute("href");
          if (url && url !== "#" && !url.startsWith("javascript")) {
            // Professional: Redirection-ah trigger pannittu menu-va force-aa hide panrom
            window.location.assign(url);
            menu.classList.remove("show");
            return;
          }
        }

        // CASE B: Logout Form
        if (button && button.type === "submit") {
          const form = button.closest("form");
          if (form) {
            form.submit();
            menu.classList.remove("show");
          }
        }
      });
    }
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
