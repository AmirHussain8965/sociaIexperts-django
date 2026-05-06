document.addEventListener("DOMContentLoaded", function () {
    const toggler = document.getElementById("sidebarToggler");
    const sidebar = document.getElementById("sidebar");
    
    if (toggler && sidebar) {
        toggler.addEventListener("click", function () {
            sidebar.classList.toggle("active");
        });
    }

    // Close sidebar when clicking outside on mobile
    document.addEventListener("click", function(event) {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(event.target) && !toggler.contains(event.target)) {
                sidebar.classList.remove("active");
            }
        }
    });
});
