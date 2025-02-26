document.addEventListener('DOMContentLoaded', () => {
    // Add mobile menu toggle button if needed
    const topNav = document.querySelector('.top-nav');
    if (window.innerWidth <= 768 && !document.querySelector('.mobile-menu-toggle')) {
        const mobileMenuToggle = document.createElement('button');
        mobileMenuToggle.className = 'mobile-menu-toggle';
        mobileMenuToggle.innerHTML = '<i class="fas fa-bars"></i>';
        topNav.insertBefore(mobileMenuToggle, topNav.firstChild);

        // Toggle mobile menu
        mobileMenuToggle.addEventListener('click', () => {
            const sideNav = document.querySelector('.side-nav');
            sideNav.classList.toggle('show');
        });
    }

    // Handle dropdown menu toggle
    const avatarBtn = document.querySelector('.avatar-btn');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    if (avatarBtn && dropdownMenu) {
        // For mobile/tablet where hover doesn't work well
        avatarBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', () => {
            dropdownMenu.style.display = 'none';
        });
    }

    // Highlight active nav link
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;

    navLinks.forEach((link) => {
        const href = link.getAttribute('href');
        if (href === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // Highlight active side nav link
    const sideNavLinks = document.querySelectorAll('.side-nav-link');

    sideNavLinks.forEach((link) => {
        const href = link.getAttribute('href');
        if (href === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});
