// main script
(function () {
  "use strict";

  // Testimonial Slider
  // ----------------------------------------
  if (typeof window.Swiper !== "undefined") {
    new Swiper(".testimonial-slider", {
      spaceBetween: 24,
      loop: true,
      pagination: {
        el: ".testimonial-slider-pagination",
        type: "bullets",
        clickable: true,
      },
      breakpoints: {
        768: {
          slidesPerView: 2,
        },
        992: {
          slidesPerView: 3,
        },
      },
    });
  }

  // Featured project carousel
  // ----------------------------------------
  const projectCarousel = document.querySelector("[data-project-carousel]");
  if (projectCarousel && typeof window.Swiper !== "undefined") {
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    const toggle = projectCarousel.querySelector("[data-project-toggle]");
    const pauseLabel = toggle?.dataset.pauseLabel || "Pause slides";
    const resumeLabel = toggle?.dataset.resumeLabel || "Resume slides";
    let manuallyPaused = false;
    let pointerInside = false;
    let focusWithin = false;
    let carousel;

    const updateAutoplay = () => {
      if (!carousel?.autoplay) return;

      if (document.hidden || reducedMotion.matches || manuallyPaused || pointerInside || focusWithin) {
        carousel.autoplay.stop();
      } else {
        carousel.autoplay.start();
      }
    };

    const updateToggle = () => {
      if (!toggle) return;
      toggle.textContent = manuallyPaused ? resumeLabel : pauseLabel;
      toggle.setAttribute("aria-label", manuallyPaused ? resumeLabel : pauseLabel);
      toggle.setAttribute("aria-pressed", String(manuallyPaused));
    };

    carousel = new Swiper(projectCarousel, {
      slidesPerView: 1,
      spaceBetween: 24,
      loop: true,
      autoHeight: true,
      speed: 550,
      autoplay: {
        delay: 7000,
        disableOnInteraction: false,
        pauseOnMouseEnter: false,
      },
      navigation: {
        prevEl: projectCarousel.querySelector("[data-project-prev]"),
        nextEl: projectCarousel.querySelector("[data-project-next]"),
      },
      pagination: {
        el: projectCarousel.querySelector("[data-project-pagination]"),
        type: "bullets",
        clickable: true,
      },
      keyboard: {
        enabled: true,
        onlyInViewport: true,
      },
    });

    projectCarousel.addEventListener("mouseenter", () => {
      pointerInside = true;
      updateAutoplay();
    });
    projectCarousel.addEventListener("mouseleave", () => {
      pointerInside = false;
      updateAutoplay();
    });
    projectCarousel.addEventListener("focusin", () => {
      focusWithin = true;
      updateAutoplay();
    });
    projectCarousel.addEventListener("focusout", (event) => {
      if (!projectCarousel.contains(event.relatedTarget)) {
        focusWithin = false;
        updateAutoplay();
      }
    });
    document.addEventListener("visibilitychange", updateAutoplay);
    reducedMotion.addEventListener?.("change", updateAutoplay);

    toggle?.addEventListener("click", () => {
      manuallyPaused = !manuallyPaused;
      if (!manuallyPaused) {
        focusWithin = false;
        pointerInside = false;
      }
      updateToggle();
      updateAutoplay();
    });

    updateToggle();
    updateAutoplay();
  }
})();
