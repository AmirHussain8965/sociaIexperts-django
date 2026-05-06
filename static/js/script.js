// =============================================
//  Solution Experts - Main JavaScript
// =============================================
//  1. Navbar Scroll Effect
//  2. Back To Top Button
//  3. Sidebar Offcanvas Toggle
//  4. Search Popup Toggle
//  5. Brand Logo Slider (Swiper)
//  6. AOS Animations Init
//  7. Smooth Scroll & Active Nav Link
// =============================================


// 1. Navbar Scroll Effect ==================================

window.addEventListener("scroll", function () {
    const header = document.querySelector(".header_section");
    if (window.scrollY > 50) {
        header.classList.add("scrolled");
    } else {
        header.classList.remove("scrolled");
    }
});


// 2. Back To Top Button ====================================

document.addEventListener("DOMContentLoaded", function () {
    const backToTopBtn = document.getElementById("backToTop");

    window.addEventListener("scroll", () => {
        if (window.scrollY > 300) {
            backToTopBtn.classList.add("show");
        } else {
            backToTopBtn.classList.remove("show");
        }
    });

    backToTopBtn.addEventListener("click", () => {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });
});


// 3. Sidebar Offcanvas Toggle ==============================

document.addEventListener("DOMContentLoaded", function () {
    const sidebarToggle = document.getElementById("sidebarToggle");
    const sidebar = document.getElementById("offcanvasSidebar");
    const sidebarClose = document.getElementById("offcanvasClose");
    const overlay = document.getElementById("bodyOverlay");

    function openSidebar() {
        sidebar.classList.add("opened");
        overlay.classList.add("active");
        document.body.style.overflow = "hidden";
    }

    function closeSidebar() {
        sidebar.classList.remove("opened");
        overlay.classList.remove("active");
        document.body.style.overflow = "";
    }

    sidebarToggle.addEventListener("click", openSidebar);
    sidebarClose.addEventListener("click", closeSidebar);
    overlay.addEventListener("click", closeSidebar);

    // Close on Escape key
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && sidebar.classList.contains("opened")) {
            closeSidebar();
        }
    });
});


// 4. Search Popup Toggle ===================================

document.addEventListener("DOMContentLoaded", function () {
    const searchToggle = document.getElementById("searchToggle");
    const searchPopup = document.getElementById("searchPopup");
    const searchClose = document.getElementById("searchClose");

    function openSearch() {
        searchPopup.classList.add("active");
        document.body.style.overflow = "hidden";
        setTimeout(() => {
            searchPopup.querySelector("input").focus();
        }, 300);
    }

    function closeSearch() {
        searchPopup.classList.remove("active");
        document.body.style.overflow = "";
    }

    searchToggle.addEventListener("click", openSearch);
    searchClose.addEventListener("click", closeSearch);

    // Close on Escape key
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && searchPopup.classList.contains("active")) {
            closeSearch();
        }
    });

    // Close when clicking outside the form
    searchPopup.addEventListener("click", function (e) {
        if (e.target === searchPopup) {
            closeSearch();
        }
    });
});


// 5. Brand Logo Slider (Swiper) ============================

document.addEventListener("DOMContentLoaded", function () {
    if (typeof Swiper !== "undefined") {
        new Swiper(".brand_slider", {
            slidesPerView: 2,
            spaceBetween: 30,
            loop: true,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false
            },
            speed: 800,
            breakpoints: {
                576: { slidesPerView: 3 },
                768: { slidesPerView: 4 },
                992: { slidesPerView: 5 },
                1200: { slidesPerView: 6 }
            }
        });
    }
});


// 6. AOS Animations Init ===================================

document.addEventListener("DOMContentLoaded", function () {
    if (typeof AOS !== "undefined") {
        AOS.init({
            duration: 1000,
            easing: "ease-out",
            once: true,
            offset: 80,
            disable: function () {
                return window.innerWidth < 576;
            }
        });
    }
});


// 7. Smooth Scroll & Active Nav Link =======================

document.addEventListener("DOMContentLoaded", function () {
    const navLinks = document.querySelectorAll(".nav_link");

    navLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            const href = this.getAttribute("href");

            if (href.startsWith("#") && href.length > 1) {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();

                    // Update active state
                    navLinks.forEach(l => l.classList.remove("active"));
                    this.classList.add("active");

                    // Smooth scroll with header offset
                    const headerHeight = document.querySelector(".header_section").offsetHeight;
                    const targetTop = target.getBoundingClientRect().top + window.scrollY - headerHeight - 20;

                    window.scrollTo({
                        top: targetTop,
                        behavior: "smooth"
                    });

                    // Close mobile menu if open
                    const navCollapse = document.getElementById("mainNav");
                    if (navCollapse && navCollapse.classList.contains("show")) {
                        navCollapse.classList.remove("show");
                    }
                }
            }
        });
    });

    // Update active link based on scroll position
    const sections = document.querySelectorAll("section[id]");

    window.addEventListener("scroll", function () {
        const scrollPos = window.scrollY + 150;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute("id");

            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove("active");
                    if (link.getAttribute("href") === "#" + sectionId) {
                        link.classList.add("active");
                    }
                });
            }
        });
    });
});


// 8. Counter Animation =====================================

document.addEventListener("DOMContentLoaded", function () {
    const counters = document.querySelectorAll(".counter_value");

    if (counters.length === 0) return;

    function animateCounter(el) {
        const target = parseInt(el.getAttribute("data-target"));
        const duration = 2000;
        const stepTime = 16;
        const totalSteps = duration / stepTime;
        const increment = target / totalSteps;
        let current = 0;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = Math.floor(current).toLocaleString();
        }, stepTime);
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.4 });

    counters.forEach(c => observer.observe(c));
});


// 9. Portfolio Slider (About Page) =========================

document.addEventListener("DOMContentLoaded", function () {
    const portfolioEl = document.querySelector(".portfolio_slider");

    if (portfolioEl && typeof Swiper !== "undefined") {
        new Swiper(".portfolio_slider", {
            slidesPerView: 1,
            spaceBetween: 20,
            loop: true,
            centeredSlides: true,
            speed: 800,
            autoplay: {
                delay: 3500,
                disableOnInteraction: false
            },
            breakpoints: {
                576: { slidesPerView: 1.5, centeredSlides: true },
                768: { slidesPerView: 2, centeredSlides: false },
                992: { slidesPerView: 2.5, centeredSlides: true },
                1200: { slidesPerView: 3, centeredSlides: true }
            }
        });
    }
});


// 10. Trusted Testimonial Slider (About Page) ==============

document.addEventListener("DOMContentLoaded", function () {
    const trustedEl = document.querySelector(".trusted_slider");

    if (trustedEl && typeof Swiper !== "undefined") {
        new Swiper(".trusted_slider", {
            slidesPerView: 1,
            spaceBetween: 25,
            loop: true,
            speed: 800,
            autoplay: {
                delay: 4000,
                disableOnInteraction: false
            },
            breakpoints: {
                576: { slidesPerView: 2 },
                992: { slidesPerView: 3 },
                1200: { slidesPerView: 4 }
            }
        });
    }
});


// 11. Password Toggle (Auth Pages) =========================

document.addEventListener("DOMContentLoaded", function () {
    const toggles = document.querySelectorAll(".password_toggle");

    toggles.forEach(btn => {
        btn.addEventListener("click", function () {
            const targetId = this.getAttribute("data-target");
            const input = document.getElementById(targetId);
            const icon = this.querySelector("i");

            if (input.type === "password") {
                input.type = "text";
                icon.classList.remove("bi-eye");
                icon.classList.add("bi-eye-slash");
            } else {
                input.type = "password";
                icon.classList.remove("bi-eye-slash");
                icon.classList.add("bi-eye");
            }
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const userBtn = document.getElementById('userDropdown');
    const userMenu = document.getElementById('userMenu');
    const parentLi = userBtn.parentElement;

    userBtn.addEventListener('click', function(e) {
        e.preventDefault();
        // Toggle menu and arrow rotation
        userMenu.classList.toggle('show');
        parentLi.classList.toggle('active_toggle');
    });

    // Close dropdown when clicking outside
    window.addEventListener('click', function(e) {
        if (!parentLi.contains(e.target)) {
            userMenu.classList.remove('show');
            parentLi.classList.remove('active_toggle');
        }
    });
});