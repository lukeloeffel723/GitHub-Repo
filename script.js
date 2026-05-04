// =============================================
// APEX PRESSURE WASHING — MAIN SCRIPT
// =============================================

document.addEventListener('DOMContentLoaded', function () {

  // ---- Sticky header shadow ----
  const header = document.getElementById('header');
  window.addEventListener('scroll', function () {
    header.classList.toggle('scrolled', window.scrollY > 10);
  }, { passive: true });

  // ---- Mobile nav toggle ----
  const hamburger = document.getElementById('hamburger');
  const mobileNav = document.getElementById('mobile-nav');

  hamburger.addEventListener('click', function () {
    const isOpen = mobileNav.classList.toggle('open');
    hamburger.classList.toggle('open', isOpen);
    hamburger.setAttribute('aria-expanded', isOpen);
    mobileNav.setAttribute('aria-hidden', !isOpen);
  });

  // Close mobile nav when a link is clicked
  document.querySelectorAll('.mobile-nav-link, .mobile-cta').forEach(function (link) {
    link.addEventListener('click', function () {
      mobileNav.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
      mobileNav.setAttribute('aria-hidden', 'true');
    });
  });

  // ---- Scroll-based entrance animations ----
  const animatableSelectors = [
    '.service-card',
    '.feature-item',
    '.gallery-card',
    '.testimonial-card',
    '.about-stat-card',
  ];

  const allAnimatable = document.querySelectorAll(animatableSelectors.join(','));

  allAnimatable.forEach(function (el) {
    el.classList.add('animate-hidden');
  });

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.remove('animate-hidden');
        entry.target.classList.add('animate-in');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  allAnimatable.forEach(function (el) { observer.observe(el); });

  // ---- Quote form validation and submission ----
  const form = document.getElementById('quoteForm');
  const submitBtn = document.getElementById('submitBtn');
  const successModal = document.getElementById('successModal');
  const closeModal = document.getElementById('closeModal');

  function showError(fieldId, message) {
    const errorEl = document.getElementById(fieldId + 'Error');
    const input = document.getElementById(fieldId);
    if (errorEl) errorEl.textContent = message;
    if (input) input.classList.add('error');
  }

  function clearError(fieldId) {
    const errorEl = document.getElementById(fieldId + 'Error');
    const input = document.getElementById(fieldId);
    if (errorEl) errorEl.textContent = '';
    if (input) input.classList.remove('error');
  }

  function validateForm() {
    let valid = true;

    // First name
    const firstName = document.getElementById('firstName').value.trim();
    clearError('firstName');
    if (!firstName) { showError('firstName', 'Please enter your first name.'); valid = false; }

    // Last name
    const lastName = document.getElementById('lastName').value.trim();
    clearError('lastName');
    if (!lastName) { showError('lastName', 'Please enter your last name.'); valid = false; }

    // Phone
    const phone = document.getElementById('phone').value.trim();
    clearError('phone');
    const phoneDigits = phone.replace(/\D/g, '');
    if (!phone) {
      showError('phone', 'Please enter your phone number.'); valid = false;
    } else if (phoneDigits.length < 10) {
      showError('phone', 'Please enter a valid 10-digit phone number.'); valid = false;
    }

    // Email (optional but validate format if provided)
    const email = document.getElementById('email').value.trim();
    clearError('email');
    if (email) {
      const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRe.test(email)) { showError('email', 'Please enter a valid email address.'); valid = false; }
    }

    // Address
    const address = document.getElementById('address').value.trim();
    clearError('address');
    if (!address) { showError('address', 'Please enter your property address.'); valid = false; }

    // Services
    const services = document.querySelectorAll('input[name="services"]:checked');
    const servicesError = document.getElementById('servicesError');
    if (services.length === 0) {
      if (servicesError) servicesError.textContent = 'Please select at least one service.';
      valid = false;
    } else {
      if (servicesError) servicesError.textContent = '';
    }

    return valid;
  }

  // Live clear errors on input
  ['firstName', 'lastName', 'phone', 'email', 'address'].forEach(function (id) {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('input', function () { clearError(id); });
    }
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    if (!validateForm()) return;

    // Show loading state
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;

    // Simulate async submission (replace with real endpoint as needed)
    setTimeout(function () {
      submitBtn.classList.remove('loading');
      submitBtn.disabled = false;
      form.reset();

      // Show success modal
      successModal.classList.add('visible');
      successModal.setAttribute('aria-hidden', 'false');
      closeModal.focus();
    }, 1200);
  });

  // Close modal
  function hideModal() {
    successModal.classList.remove('visible');
    successModal.setAttribute('aria-hidden', 'true');
  }

  closeModal.addEventListener('click', hideModal);

  successModal.addEventListener('click', function (e) {
    if (e.target === successModal) hideModal();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && successModal.classList.contains('visible')) hideModal();
  });

  // ---- Smooth scroll for anchor links ----
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const headerHeight = header.offsetHeight;
        const targetTop = target.getBoundingClientRect().top + window.scrollY - headerHeight - 12;
        window.scrollTo({ top: targetTop, behavior: 'smooth' });
      }
    });
  });

  // ---- Active nav link highlight ----
  const sections = document.querySelectorAll('section[id], footer[id]');
  const navLinks = document.querySelectorAll('#nav a');

  const sectionObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        navLinks.forEach(function (link) {
          link.style.color = '';
          link.style.background = '';
          if (link.getAttribute('href') === '#' + entry.target.id) {
            link.style.color = '#1a56db';
            link.style.background = '#eff6ff';
          }
        });
      }
    });
  }, { threshold: 0.4 });

  sections.forEach(function (section) { sectionObserver.observe(section); });

});
