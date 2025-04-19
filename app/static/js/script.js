// static/js/script.js

document.addEventListener("DOMContentLoaded", function() {
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add animation to elements with 'animated' class
    const animated = document.querySelectorAll('.animated');
    if (animated.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    observer.unobserve(entry.target);
                }
            });
        });

        animated.forEach(item => {
            observer.observe(item);
        });
    }

    // Initialize skill chart if on the homepage
    const skillsSection = document.getElementById('skills-chart');
    if (skillsSection) {
        fetch('/api/skills')
            .then(response => response.json())
            .then(data => {
                // Group skills by category
                const categories = {};
                data.forEach(skill => {
                    if (!categories[skill.category]) {
                        categories[skill.category] = [];
                    }
                    categories[skill.category].push(skill);
                });

                // Create charts for each category
                Object.keys(categories).forEach(category => {
                    const categorySkills = categories[category];
                    const chartContainer = document.createElement('div');
                    chartContainer.className = 'mb-4';

                    const title = document.createElement('h4');
                    title.textContent = category;
                    chartContainer.appendChild(title);

                    categorySkills.forEach(skill => {
                        const skillContainer = document.createElement('div');
                        skillContainer.className = 'mb-3';

                        const labelContainer = document.createElement('div');
                        labelContainer.className = 'd-flex justify-content-between mb-1';

                        const nameSpan = document.createElement('span');
                        nameSpan.textContent = skill.name;

                        const valueSpan = document.createElement('span');
                        valueSpan.textContent = `${skill.proficiency}%`;

                        labelContainer.appendChild(nameSpan);
                        labelContainer.appendChild(valueSpan);

                        const progressContainer = document.createElement('div');
                        progressContainer.className = 'progress';

                        const progressBar = document.createElement('div');
                        progressBar.className = 'progress-bar';
                        progressBar.setAttribute('role', 'progressbar');
                        progressBar.style.width = `${skill.proficiency}%`;

                        progressContainer.appendChild(progressBar);

                        skillContainer.appendChild(labelContainer);
                        skillContainer.appendChild(progressContainer);

                        chartContainer.appendChild(skillContainer);
                    });

                    skillsSection.appendChild(chartContainer);
                });
            })
            .catch(error => console.error('Error loading skills:', error));
    }

    // Contact form validation
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            const subjectInput = document.getElementById('subject');
            const contentInput = document.getElementById('content');

            let valid = true;

            // Very basic validation
            if (!nameInput.value.trim()) {
                showError(nameInput, 'Name is required');
                valid = false;
            } else {
                removeError(nameInput);
            }

            if (!emailInput.value.trim()) {
                showError(emailInput, 'Email is required');
                valid = false;
            } else if (!isValidEmail(emailInput.value)) {
                showError(emailInput, 'Please enter a valid email');
                valid = false;
            } else {
                removeError(emailInput);
            }

            if (!subjectInput.value.trim()) {
                showError(subjectInput, 'Subject is required');
                valid = false;
            } else {
                removeError(subjectInput);
            }

            if (!contentInput.value.trim()) {
                showError(contentInput, 'Message is required');
                valid = false;
            } else {
                removeError(contentInput);
            }

            if (!valid) {
                e.preventDefault();
            }
        });
    }

    // Helper functions
    function showError(input, message) {
        const formGroup = input.parentElement;
        const errorDiv = formGroup.querySelector('.invalid-feedback') || document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;

        input.classList.add('is-invalid');

        if (!formGroup.querySelector('.invalid-feedback')) {
            formGroup.appendChild(errorDiv);
        }
    }

    function removeError(input) {
        input.classList.remove('is-invalid');
        const formGroup = input.parentElement;
        const errorDiv = formGroup.querySelector('.invalid-feedback');
        if (errorDiv) {
            formGroup.removeChild(errorDiv);
        }
    }

    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
});