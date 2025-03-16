# REALdegrees Website

A professional website for REALdegrees, providing human solutions for the AI crisis in education.

## Overview

This is a clean, responsive website designed for REALdegrees. It serves as an informational landing page to showcase educational services, philosophy, and contact information for addressing challenges of AI in education.

## Features

- Responsive design that works on all devices
- Modern, professional UI
- Single-page layout with smooth scrolling navigation
- Contact form with client-side validation
- Optimized for fast loading
- SEO-friendly structure

## Technologies Used

- HTML5
- CSS3 (with CSS variables)
- JavaScript (vanilla JS, no frameworks)
- Font Awesome for icons
- Google Fonts

## Project Structure

```
RDwebsite/
├── css/
│   ├── normalize.css
│   └── styles.css
├── js/
│   └── main.js
├── images/
├── index.html
├── robots.txt
├── CNAME
└── README.md
```

## Setup and Deployment

### Local Development

1. Clone the repository
2. Open the project in your favorite code editor
3. You can run the website locally by opening `index.html` in your browser

### Deployment on GitHub Pages

1. Push your code to a GitHub repository
2. Go to the repository settings
3. Scroll down to the GitHub Pages section
4. Select the branch you want to deploy (usually `main` or `master`)
5. The site will be published at `https://username.github.io/repository`

### Custom Domain Setup

1. Update the `CNAME` file with your actual domain name
2. In your Dynadot account, set up the following DNS records:
   - A record: `@` pointing to `185.199.108.153`
   - A record: `@` pointing to `185.199.109.153`
   - A record: `@` pointing to `185.199.110.153`
   - A record: `@` pointing to `185.199.111.153`
   - CNAME record: `www` pointing to `username.github.io`
3. In your GitHub repository settings, add your custom domain
4. Check "Enforce HTTPS" for secure connections

## Expanding the Website

This website is designed to be easily expandable. Here are some tips for adding new content:

- Add new pages by creating HTML files and linking them in the navigation
- Add new sections by following the existing structure patterns
- Extend the CSS with new style rules as needed
- Add more JavaScript functionality in the main.js file or create new JS files

## License

[MIT License](LICENSE)

## Contact

For questions or support, please reach out to your contact information.
