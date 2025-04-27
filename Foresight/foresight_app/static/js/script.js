window.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.fade-in-up');
  
    animatedElements.forEach(el => {
      const delay = el.classList.contains('delay-1') ? 500 :
                    el.classList.contains('delay-2') ? 1000 : 0;
  
      setTimeout(() => {
        el.style.animationPlayState = 'running';
      }, delay);
    });
  });
  

  const menuToggle = document.getElementById("menu-toggle");
  const menuClose = document.getElementById("menu-close");
  const navLinks = document.getElementById("nav-links");    
  const socialSidebar = document.querySelector(".social-sidebar");
  
  if (menuToggle && menuClose && navLinks) {
    menuToggle.addEventListener("click", function () {
      navLinks.classList.add("active");
      socialSidebar?.classList.add("move-left");
    });
  
    menuClose.addEventListener("click", () => {
      navLinks.classList.remove("active");
      socialSidebar?.classList.remove("move-left");
    });
  
    document.querySelectorAll("#nav-links a").forEach(link => {
      link.addEventListener("click", () => {
        navLinks.classList.remove("active");
        socialSidebar?.classList.remove("move-left");
      });
    });
  
    document.addEventListener("click", (event) => {
      const isClickInside = navLinks.contains(event.target) || menuToggle.contains(event.target);
      if (!isClickInside && navLinks.classList.contains("active")) {
        navLinks.classList.remove("active");
        socialSidebar?.classList.remove("move-left");
      }
    });
  }
  