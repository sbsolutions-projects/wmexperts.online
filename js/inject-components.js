/**
 * Lightweight Header/Footer Injector for Static Sites
 * Use this if you prefer client-side injection (alternative to Python build script)
 * 
 * SEO Considerations:
 * - This uses async loading to prevent blocking page render
 * - HTTP headers should include preload hints for critical content
 * - Only use this if header/footer aren't critical for initial SEO
 * 
 * Usage:
 * 1. Add this script at the END of your <body> tag (before closing </body>)
 * 2. Add empty <header id="header-container"></header> where your header should go
 * 3. Add empty <footer id="footer-container"></footer> where your footer should go
 * 
 * Example:
 * <body>
 *     <header id="header-container"></header>
 *     <!-- page content -->
 *     <footer id="footer-container"></footer>
 *     <script src="js/inject-components.js" async></script>
 * </body>
 */

async function injectComponents() {
    const componentsPath = 'templates/';
    
    // Fetch and inject header
    const headerContainer = document.getElementById('header-container');
    if (headerContainer) {
        try {
            const response = await fetch(`${componentsPath}header.html`);
            if (response.ok) {
                headerContainer.innerHTML = await response.text();
                // Set active nav link based on current page
                setActiveNavLink();
            }
        } catch (error) {
            console.warn('Failed to load header:', error);
        }
    }
    
    // Fetch and inject footer
    const footerContainer = document.getElementById('footer-container');
    if (footerContainer) {
        try {
            const response = await fetch(`${componentsPath}footer.html`);
            if (response.ok) {
                footerContainer.innerHTML = await response.text();
            }
        } catch (error) {
            console.warn('Failed to load footer:', error);
        }
    }
}

function setActiveNavLink() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage || (currentPage === '' && href === 'index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Inject components when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectComponents);
} else {
    injectComponents();
}
