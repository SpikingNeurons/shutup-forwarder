/* ─── NAV SCROLL EFFECT ──────────────────────────────────────────── */
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 10);
});

/* ─── MOBILE BURGER ──────────────────────────────────────────────── */
const burger = document.getElementById('burger');
const navLinks = document.querySelector('.nav__links');
const navActions = document.querySelector('.nav__actions');

burger.addEventListener('click', () => {
  navLinks.classList.toggle('open');
  navActions.classList.toggle('open');
});

// Close on link click
document.querySelectorAll('.nav__links a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    navActions.classList.remove('open');
  });
});

/* ─── SCROLL REVEAL ──────────────────────────────────────────────── */
const revealTargets = [
  '.step',
  '.feature-card',
  '.evidence-step',
  '.for-who-card',
  '.testimonial',
  '.section-label',
  '.section-title',
  '.section-sub',
  '.evidence-chain',
  '.driver-perks',
  '.protection-note',
];

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
);

revealTargets.forEach((selector) => {
  document.querySelectorAll(selector).forEach((el, i) => {
    el.classList.add('reveal');
    // stagger children of the same parent
    el.style.transitionDelay = `${i * 80}ms`;
    revealObserver.observe(el);
  });
});

/* ─── QUOTE FORM SUBMIT ──────────────────────────────────────────── */
const quoteSubmit = document.querySelector('.quote-submit');
if (quoteSubmit) {
  quoteSubmit.addEventListener('click', (e) => {
    e.preventDefault();
    const inputs = document.querySelectorAll('.quote-field input');
    let valid = true;
    inputs.forEach((input) => {
      if (!input.value.trim()) {
        input.style.borderColor = '#f87171';
        valid = false;
      } else {
        input.style.borderColor = '';
      }
    });
    if (valid) {
      quoteSubmit.textContent = '✅ Request received!';
      quoteSubmit.disabled = true;
      setTimeout(() => {
        quoteSubmit.textContent = 'Get my quote →';
        quoteSubmit.disabled = false;
        inputs.forEach((input) => { input.value = ''; });
      }, 3000);
    }
  });
}

/* ─── SMOOTH ACTIVE NAV HIGHLIGHT ────────────────────────────────── */
const sections = document.querySelectorAll('section[id]');
const navAnchors = document.querySelectorAll('.nav__links a[href^="#"]');

const sectionObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        navAnchors.forEach((a) => {
          a.style.color = '';
          if (a.getAttribute('href') === `#${entry.target.id}`) {
            a.style.color = 'var(--c-primary)';
          }
        });
      }
    });
  },
  { threshold: 0.4 }
);

sections.forEach((s) => sectionObserver.observe(s));
