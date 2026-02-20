document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide Icons
    lucide.createIcons();

    // Scroll Animation Observer
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in-section').forEach(section => {
        observer.observe(section);
    });

    // Navbar Scroll Effect
    const navbar = document.querySelector('.navbar-fixed');
    const brandLogo = document.querySelector('.brand-logo');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            navbar.classList.add('glass-header', 'py-4');
            navbar.classList.remove('bg-transparent', 'py-6');
            if (brandLogo) brandLogo.classList.add('scale-90');
        } else {
            navbar.classList.add('bg-transparent', 'py-6');
            navbar.classList.remove('glass-header', 'py-4');
            if (brandLogo) brandLogo.classList.remove('scale-90');
        }
    });

    // Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const closeMenuBtn = document.getElementById('close-menu-btn');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.remove('hidden');
            setTimeout(() => {
                mobileMenu.classList.remove('opacity-0', 'translate-x-full');
            }, 10);
        });

        closeMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.add('opacity-0', 'translate-x-full');
            setTimeout(() => {
                mobileMenu.classList.add('hidden');
            }, 300);
        });
    }

    // Number Counter Animation
    const counters = document.querySelectorAll('.counter');
    const counterObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute('data-target'));
                const duration = 2000; // 2 seconds
                let startTimestamp = null;

                const step = (timestamp) => {
                    if (!startTimestamp) startTimestamp = timestamp;
                    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                    entry.target.innerText = Math.floor(progress * target).toLocaleString() + (target > 100 ? '+' : '');

                    if (progress < 1) {
                        window.requestAnimationFrame(step);
                    }
                };

                window.requestAnimationFrame(step);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => counterObserver.observe(counter));
    // Lead Generation Popup Logic
    const leadPopup = document.getElementById('lead-popup');
    const closePopupBtn = document.getElementById('close-popup-btn');
    const leadPopupContent = document.getElementById('lead-popup-content');

    if (leadPopup && closePopupBtn) {

        const showPopup = () => {
            // Check if user has already closed it in this session
            if (!sessionStorage.getItem('popupClosed') && !window.popupShown) {
                leadPopup.classList.remove('opacity-0', 'pointer-events-none');
                leadPopupContent.classList.remove('scale-95');
                leadPopupContent.classList.add('scale-100');
                window.popupShown = true; // Mark as shown for this page load
            }
        };

        // Trigger 1: Show popup after 5 seconds
        setTimeout(showPopup, 5000);

        // Trigger 2: Exit Intent (Mouse leaves the viewport)
        document.addEventListener('mouseleave', (e) => {
            if (e.clientY <= 0) { // Only trigger if mouse leaves from the TOP
                showPopup();
            }
        });

        // Close popup function
        const closePopup = () => {
            leadPopup.classList.add('opacity-0', 'pointer-events-none');
            leadPopupContent.classList.add('scale-95');
            leadPopupContent.classList.remove('scale-100');
            sessionStorage.setItem('popupClosed', 'true'); // Remember it's closed for this session
        };

        closePopupBtn.addEventListener('click', closePopup);

        // Close if clicking outside the content
        leadPopup.addEventListener('click', (e) => {
            if (e.target === leadPopup) {
                closePopup();
            }
        });
    }
});
