// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Search input focus effect
  const searchInput = document.querySelector('.search-bar input');
  if (searchInput) {
    searchInput.addEventListener('focus', function() {
      this.parentElement.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.3)';
    });
    
    searchInput.addEventListener('blur', function() {
      this.parentElement.style.boxShadow = 'none';
    });
  }

  // Product card hover shimmer effect
  document.querySelectorAll('.product-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
      const image = this.querySelector('.product-image');
      if (image) {
        image.style.background = 'linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent)';
        image.style.backgroundSize = '200% 100%';
        image.style.animation = 'shimmer 1.5s infinite';
      }
    });
    
    card.addEventListener('mouseleave', function() {
      const image = this.querySelector('.product-image');
      if (image) {
        image.style.background = '';
        image.style.animation = '';
      }
    });
  });

  // Add shimmer animation to CSS (dynamically)
  if (!document.querySelector('#shimmer-style')) {
    const style = document.createElement('style');
    style.id = 'shimmer-style';
    style.textContent = `
      @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
      }
    `;
    document.head.appendChild(style);
  }

  // Intersection Observer for fade-in animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Observe product cards and sidebar
  document.querySelectorAll('.product-card, .catalog-sidebar').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1), transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
    observer.observe(el);
  });

  // Navbar scroll effect
  let lastScrollY = window.scrollY;
  window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
      navbar.style.background = 'rgba(15, 15, 35, 0.98)';
      navbar.style.backdropFilter = 'blur(30px)';
    } else {
      navbar.style.background = 'rgba(15, 15, 35, 0.95)';
      navbar.style.backdropFilter = 'blur(20px)';
    }
    
    // Navbar hide/show on scroll
    if (window.scrollY > lastScrollY && window.scrollY > 100) {
      navbar.style.transform = 'translateY(-100%)';
    } else {
      navbar.style.transform = 'translateY(0)';
    }
    lastScrollY = window.scrollY;
  });

  // Add to cart button simulation (if needed)
  document.querySelectorAll('.btn-primary').forEach(btn => {
    btn.addEventListener('click', function(e) {
      // Add ripple effect
      const ripple = document.createElement('span');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      
      ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255,255,255,0.5);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
      `;
      
      this.style.position = 'relative';
      this.style.overflow = 'hidden';
      this.appendChild(ripple);
      
      setTimeout(() => ripple.remove(), 600);
    });
  });
});
// Add to static/js/script.js - Additional functionality

// Cart quantity controls with loading states
document.addEventListener('DOMContentLoaded', function() {
  // Cart quantity buttons
  document.querySelectorAll('.qty-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const href = this.getAttribute('href');
      const qtyValue = this.parentElement.querySelector('.qty-value');
      
      // Loading state
      this.style.transform = 'scale(0.95)';
      this.style.opacity = '0.7';
      
      setTimeout(() => {
        window.location.href = href;
      }, 150);
    });
  });

  // Remove item confirmation
  document.querySelectorAll('.remove-link').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      if (confirm('Remove this item from cart?')) {
        window.location.href = this.getAttribute('href');
      }
    });
  });

  // Form input floating labels effect
  document.querySelectorAll('.form-field input').forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement.classList.add('focused');
    });
    
    input.addEventListener('blur', function() {
      if (!this.value) {
        this.parentElement.classList.remove('focused');
      }
    });
    
    if (input.value) {
      input.parentElement.classList.add('focused');
    }
  });

  // Product image zoom on hover
  const productMainImage = document.querySelector('.product-main-image img');
  if (productMainImage) {
    productMainImage.parentElement.addEventListener('mousemove', function(e) {
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      productMainImage.style.transform = scale(1.1) translate(${x * 0.01}px, ${y * 0.01}px);
    });
    
    productMainImage.parentElement.addEventListener('mouseleave', function() {
      productMainImage.style.transform = 'scale(1)';
    });
  }

  // Auto-hide success/error messages after 5 seconds
  const messages = document.querySelector('.messages');
  if (messages) {
    setTimeout(() => {
      messages.style.opacity = '0';
      messages.style.transform = 'translateY(-20px)';
      setTimeout(() => messages.remove(), 300);
    }, 5000);
  }

  // Animate order cards on load
  document.querySelectorAll('.order-card, .cart-item-card').forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    
    setTimeout(() => {
      card.style.transition = 'opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1), transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, index * 100);
  });
});

// End of static/js/script.js