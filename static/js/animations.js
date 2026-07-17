/*
  St. Joseph International School - Animations & Interactions
  Scroll reveals, counters, header effects, smooth transitions
*/

// Initialize animations on page load
document.addEventListener('DOMContentLoaded', function() {
  initScrollReveal();
  initCounterAnimation();
  initHeaderShrink();
  initPageTransitions();
});

// ===== SCROLL REVEAL ANIMATION =====
function initScrollReveal() {
  const reveals = document.querySelectorAll('.animate-scroll-reveal, .reveal');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });

  reveals.forEach(reveal => {
    observer.observe(reveal);
  });
}

// ===== COUNTER ANIMATION =====
function initCounterAnimation() {
  const counters = document.querySelectorAll('[data-counter]');

  if (counters.length === 0) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounters(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.5
  });

  counters.forEach(counter => {
    observer.observe(counter);
  });
}

function animateCounters(container) {
  const counters = container.querySelectorAll('[data-counter-value]');

  counters.forEach(counter => {
    const target = parseInt(counter.getAttribute('data-counter-value'), 10);
    const duration = 2000;
    const start = 0;
    const startTime = performance.now();

    const updateCounter = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const current = Math.floor(start + (target - start) * progress);

      counter.textContent = current.toLocaleString();

      if (progress < 1) {
        requestAnimationFrame(updateCounter);
      }
    };

    requestAnimationFrame(updateCounter);
  });
}

// ===== HEADER SHRINK ON SCROLL =====
function initHeaderShrink() {
  const header = document.querySelector('header');
  if (!header) return;

  let lastScrollY = 0;
  let scrollTimeout;

  window.addEventListener('scroll', () => {
    lastScrollY = window.scrollY;

    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
      const scrolled = lastScrollY > 100;

      if (scrolled) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    }, 10);
  }, { passive: true });
}

// ===== PAGE TRANSITIONS =====
function initPageTransitions() {
  // Fade in page on load
  const main = document.querySelector('main') || document.body;
  main.classList.add('animate-page-fade');

  // Stagger children animations
  const children = main.querySelectorAll('> section, > div, > article');
  children.forEach((child, index) => {
    child.style.animationDelay = `${index * 50}ms`;
  });
}

// ===== SMOOTH SCROLL =====
function smoothScrollTo(element) {
  if (!element) return;
  element.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ===== BUTTON HOVER EFFECTS =====
function initButtonEffects() {
  const buttons = document.querySelectorAll('button, .btn, a.btn');

  buttons.forEach(button => {
    button.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-2px)';
    });

    button.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });

    button.addEventListener('mousedown', function() {
      this.style.transform = 'translateY(0)';
    });
  });
}

// ===== CARD HOVER EFFECTS =====
function initCardEffects() {
  const cards = document.querySelectorAll('.card, .feature-card, .article-card, .stat-card');

  cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-4px)';
      this.style.boxShadow = 'var(--shadow-lg)';
    });

    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
      this.style.boxShadow = '';
    });
  });
}

// ===== ANIMATED NUMBER COUNTER =====
function countUp(element, target, duration = 2000) {
  const start = 0;
  const startTime = performance.now();

  const update = (currentTime) => {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const current = Math.floor(start + (target - start) * progress);

    element.textContent = current.toLocaleString();

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  };

  requestAnimationFrame(update);
}

// ===== SCROLL TO TOP BUTTON =====
function initScrollToTop() {
  const scrollButton = document.querySelector('[data-scroll-top]');
  if (!scrollButton) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
      scrollButton.style.display = 'block';
      scrollButton.style.opacity = '1';
    } else {
      scrollButton.style.opacity = '0';
      setTimeout(() => {
        scrollButton.style.display = 'none';
      }, 300);
    }
  }, { passive: true });

  scrollButton.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ===== INTERSECTION OBSERVER UTILITY =====
function observeElements(selector, callback, options = {}) {
  const defaultOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px',
    ...options
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        callback(entry);
      }
    });
  }, defaultOptions);

  document.querySelectorAll(selector).forEach(el => {
    observer.observe(el);
  });

  return observer;
}

// ===== FORM INTERACTIONS =====
function initFormInteractions() {
  const inputs = document.querySelectorAll('input, textarea, select');

  inputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement?.classList.add('focused');
    });

    input.addEventListener('blur', function() {
      this.parentElement?.classList.remove('focused');
    });

    input.addEventListener('input', function() {
      if (this.value) {
        this.classList.add('filled');
      } else {
        this.classList.remove('filled');
      }
    });
  });
}

// ===== LAZY LOAD IMAGES =====
function initLazyLoad() {
  const images = document.querySelectorAll('img[data-src]');

  const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.classList.add('loaded');
        imageObserver.unobserve(img);
      }
    });
  });

  images.forEach(img => {
    imageObserver.observe(img);
  });
}

// ===== TABS FUNCTIONALITY =====
function initTabs() {
  const tabButtons = document.querySelectorAll('[data-tab-button]');

  tabButtons.forEach(button => {
    button.addEventListener('click', function() {
      const tabName = this.getAttribute('data-tab-button');

      // Hide all tabs
      document.querySelectorAll('[data-tab-content]').forEach(tab => {
        tab.style.display = 'none';
        tab.classList.remove('active');
      });

      // Remove active class from all buttons
      tabButtons.forEach(btn => {
        btn.classList.remove('active');
      });

      // Show selected tab
      const selectedTab = document.querySelector(`[data-tab-content="${tabName}"]`);
      if (selectedTab) {
        selectedTab.style.display = 'block';
        selectedTab.classList.add('active');
        this.classList.add('active');
      }
    });
  });
}

// ===== ACCORDION FUNCTIONALITY =====
function initAccordion() {
  const accordionItems = document.querySelectorAll('[data-accordion-item]');

  accordionItems.forEach(item => {
    const trigger = item.querySelector('[data-accordion-trigger]');
    const content = item.querySelector('[data-accordion-content]');

    if (trigger && content) {
      trigger.addEventListener('click', function() {
        const isOpen = item.classList.contains('open');

        // Close all other accordions
        accordionItems.forEach(other => {
          if (other !== item) {
            other.classList.remove('open');
            const otherContent = other.querySelector('[data-accordion-content]');
            if (otherContent) {
              otherContent.style.maxHeight = '0';
            }
          }
        });

        // Toggle current accordion
        if (isOpen) {
          item.classList.remove('open');
          content.style.maxHeight = '0';
        } else {
          item.classList.add('open');
          content.style.maxHeight = content.scrollHeight + 'px';
        }
      });
    }
  });
}

// ===== MOBILE MENU TOGGLE =====
function initMobileMenu() {
  const menuToggle = document.querySelector('[data-mobile-menu-toggle]');
  const mobileMenu = document.querySelector('[data-mobile-menu]');

  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', () => {
      mobileMenu.classList.toggle('open');
      menuToggle.classList.toggle('active');
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('[data-mobile-menu-toggle]') && !e.target.closest('[data-mobile-menu]')) {
        mobileMenu.classList.remove('open');
        menuToggle.classList.remove('active');
      }
    });
  }
}

// ===== TOAST NOTIFICATIONS =====
function showToast(message, type = 'info', duration = 3000) {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('show');
  }, 10);

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// ===== UTILITY: PREFERS REDUCED MOTION =====
function prefersReducedMotion() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

// ===== INITIALIZE ALL =====
document.addEventListener('DOMContentLoaded', () => {
  initButtonEffects();
  initCardEffects();
  initFormInteractions();
  initLazyLoad();
  initTabs();
  initAccordion();
  initMobileMenu();
  initScrollToTop();
});

// Export functions for external use
if (typeof window !== 'undefined') {
  window.SJIS = {
    smoothScrollTo,
    countUp,
    showToast,
    observeElements,
    prefersReducedMotion,
  };
}
