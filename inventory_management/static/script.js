document.addEventListener("DOMContentLoaded", function () {
    const sidebarCollapse = document.getElementById("sidebarCollapse");
    const sidebar = document.getElementById("sidebar");

    sidebarCollapse.addEventListener("click", function () {
      sidebar.classList.toggle("active");
    });
  });