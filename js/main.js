/**
 * Main JavaScript file for RD Business Website
 * 
 * This file contains all the interactive functionality for the website.
 * - Mobile navigation toggle
 * - Smooth scrolling for navigation links
 * - Header scroll behavior
 * - Current year for footer copyright
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Cache DOM elements
    const header = document.getElementById('header');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mainNav = document.getElementById('main-nav').querySelector('ul');
    const navLinks = document.querySelectorAll('#main-nav ul li a');
    const currentYearSpan = document.getElementById('current-year');

    // Set current year in footer
    currentYearSpan.textContent = new Date().getFullYear();

    // Mobile menu toggle
    mobileMenuBtn.addEventListener('click', () => {
        mainNav.classList.toggle('show');

        // Toggle between menu and close icons
        const icon = mobileMenuBtn.querySelector('i');
        if (mainNav.classList.contains('show')) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        } else {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (event) => {
        const isClickInsideNav = mainNav.contains(event.target);
        const isClickOnMenuBtn = mobileMenuBtn.contains(event.target);

        if (!isClickInsideNav && !isClickOnMenuBtn && mainNav.classList.contains('show')) {
            mainNav.classList.remove('show');
            const icon = mobileMenuBtn.querySelector('i');
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });

    // Smooth scroll for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            // Get the target section id from href attribute
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            // Close mobile menu if open
            if (mainNav.classList.contains('show')) {
                mainNav.classList.remove('show');
                const icon = mobileMenuBtn.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }

            // Scroll to target section
            window.scrollTo({
                top: targetSection.offsetTop - header.offsetHeight,
                behavior: 'smooth'
            });

            // Update active link
            navLinks.forEach(link => link.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Header scroll behavior - add shadow and reduce size on scroll
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            header.style.padding = '5px 0';
            header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.padding = '';
            header.style.boxShadow = '';
        }

        // Update active nav link based on scroll position
        const scrollPosition = window.scrollY + header.offsetHeight + 50;

        // Get all sections
        const sections = document.querySelectorAll('section');

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;

            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                const currentId = '#' + section.getAttribute('id');
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === currentId) {
                        link.classList.add('active');
                    }
                });
            }
        });
    });
    // Accordion Functionality
    const accordionHeaders = document.querySelectorAll('.accordion-header');

    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            // Toggle active class
            header.classList.toggle('active');

            // Toggle aria-expanded
            const isExpanded = header.getAttribute('aria-expanded') === 'true';
            header.setAttribute('aria-expanded', !isExpanded);

            // Toggle content visibility
            const content = header.nextElementSibling;
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    });
});
