// FIFA World Cup 2022 Dashboard - Client-side scripts
document.addEventListener('DOMContentLoaded', function() {
    // ---------------------------------------------
    // Sticky header effect
    // ---------------------------------------------
    function handleScroll() {
        const stickyHeader = document.getElementById('sticky-header');
        
        if (stickyHeader) {
            if (window.scrollY > 60) {
                stickyHeader.classList.add('scrolled');
            } else {
                stickyHeader.classList.remove('scrolled');
            }
        }
    }

    // Add scroll event listener
    window.addEventListener('scroll', handleScroll);
    
    // Also update on initial load
    handleScroll();
    
    // ---------------------------------------------
    // Add FIFA-themed styling and animations
    // ---------------------------------------------
    
    // Add subtle entrance animations to sections
    const sections = document.querySelectorAll('.container-fluid > .row');
    let delay = 0;
    
    sections.forEach(section => {
        // Skip the header section
        if (!section.querySelector('h1')) {
            section.style.opacity = '0';
            section.style.transform = 'translateY(20px)';
            section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            
            setTimeout(() => {
                section.style.opacity = '1';
                section.style.transform = 'translateY(0)';
            }, 300 + delay);
            
            delay += 100; // Stagger the animations
        }
    });
    
    // Add smooth hover effects to graphs
    const graphContainers = document.querySelectorAll('.dash-graph');
    graphContainers.forEach(container => {
        container.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        container.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Apply FIFA theme colors to dropdown elements
    setTimeout(() => {
        const dropdownElements = document.querySelectorAll('.Select-value-label');
        dropdownElements.forEach(el => {
            el.style.color = '#326295';
            el.style.fontWeight = '500';
        });
        
        // Style dropdown placeholders
        const placeholders = document.querySelectorAll('.Select-placeholder');
        placeholders.forEach(el => {
            el.style.color = '#6c757d';
            el.style.fontStyle = 'italic';
        });
    }, 500);
    
    // Add FIFA-themed accents to charts
    const chartHeaders = document.querySelectorAll('h2, h4');
    chartHeaders.forEach(header => {
        header.innerHTML = `<span class="fifa-primary">⚽</span> ${header.innerHTML}`;
    });
    
    // Apply card container styling to graphs
    setTimeout(() => {
        const graphs = document.querySelectorAll('.js-plotly-plot');
        graphs.forEach(graph => {
            if (!graph.closest('.chart-container')) {
                const parent = graph.parentElement;
                if (parent && !parent.classList.contains('chart-container')) {
                    parent.classList.add('chart-container');
                }
            }
        });
    }, 1000);
}); 