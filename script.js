const navToggle = document.getElementById('navToggle');
const navList = document.getElementById('navList');

if (navToggle && navList) {
  navToggle.addEventListener('click', () => {
    navList.classList.toggle('nav__list--open');
  });

  navList.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      navList.classList.remove('nav__list--open');
    });
  });
}

const yearSpan = document.getElementById('year');
if (yearSpan) {
  yearSpan.textContent = String(new Date().getFullYear());
}

