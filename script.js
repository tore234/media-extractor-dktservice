document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".site-nav");
  const year = document.getElementById("year");
  const backToTop = document.querySelector(".back-to-top");
  const revealElements = document.querySelectorAll(".reveal");
  const navLinks = document.querySelectorAll(".site-nav a");

  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  const closeMenu = () => {
    if (!menuToggle || !nav) return;

    nav.classList.remove("is-open");
    menuToggle.classList.remove("is-open");
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Abrir menú de navegación");
    document.body.classList.remove("menu-open");
  };

  if (menuToggle && nav) {
    menuToggle.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("is-open");

      menuToggle.classList.toggle("is-open", isOpen);
      menuToggle.setAttribute("aria-expanded", String(isOpen));
      menuToggle.setAttribute(
        "aria-label",
        isOpen
          ? "Cerrar menú de navegación"
          : "Abrir menú de navegación"
      );

      document.body.classList.toggle("menu-open", isOpen);
    });

    navLinks.forEach((link) => {
      link.addEventListener("click", closeMenu);
    });

    document.addEventListener("click", (event) => {
      if (
        nav.classList.contains("is-open") &&
        !nav.contains(event.target) &&
        !menuToggle.contains(event.target)
      ) {
        closeMenu();
      }
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeMenu();
      }
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 820) {
        closeMenu();
      }
    });
  }

  document.querySelectorAll(".copy-btn").forEach((button) => {
    button.addEventListener("click", async () => {
      const text = button.getAttribute("data-copy") || "";
      const label = button.querySelector("span");
      const icon = button.querySelector("i");

      try {
        if (navigator.clipboard?.writeText) {
          await navigator.clipboard.writeText(text);
        } else {
          const temp = document.createElement("textarea");
          temp.value = text;
          temp.setAttribute("readonly", "");
          temp.style.position = "fixed";
          temp.style.left = "-9999px";
          document.body.appendChild(temp);
          temp.select();
          document.execCommand("copy");
          temp.remove();
        }

        button.classList.add("is-copied");

        if (label) label.textContent = "Copiado";
        if (icon) icon.className = "fa-solid fa-check";

        window.setTimeout(() => {
          button.classList.remove("is-copied");

          if (label) label.textContent = "Copiar";
          if (icon) icon.className = "fa-regular fa-copy";
        }, 1600);
      } catch {
        if (label) label.textContent = "Error";

        window.setTimeout(() => {
          if (label) label.textContent = "Copiar";
        }, 1600);
      }
    });
  });

  if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;

          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      {
        threshold: 0.12,
        rootMargin: "0px 0px -40px 0px",
      }
    );

    revealElements.forEach((element) => {
      revealObserver.observe(element);
    });
  } else {
    revealElements.forEach((element) => {
      element.classList.add("is-visible");
    });
  }

  const sections = [...document.querySelectorAll("main section[id]")];

  if ("IntersectionObserver" in window && sections.length > 0) {
    const sectionObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;

          const activeId = entry.target.id;

          navLinks.forEach((link) => {
            const href = link.getAttribute("href");
            link.classList.toggle("is-active", href === `#${activeId}`);
          });
        });
      },
      {
        threshold: 0.35,
        rootMargin: "-20% 0px -55% 0px",
      }
    );

    sections.forEach((section) => {
      sectionObserver.observe(section);
    });
  }

  if (backToTop) {
    const toggleBackToTop = () => {
      backToTop.classList.toggle("is-visible", window.scrollY > 520);
    };

    toggleBackToTop();

    window.addEventListener("scroll", toggleBackToTop, {
      passive: true,
    });

    backToTop.addEventListener("click", () => {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    });
  }
});
