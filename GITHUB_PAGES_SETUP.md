# GitHub Pages Deployment Guide

This guide outlines the steps to deploy your RD Business website to GitHub Pages and configure your custom domain from Dynadot.

## Step 1: Create a GitHub Repository

1. Sign in to your GitHub account (or create one if you don't have one)
2. Click the "+" icon in the top right corner and select "New repository"
3. Name your repository (e.g., `RDwebsite` or `yourusername.github.io` for user site)
4. Add a description (optional)
5. Choose "Public" visibility (GitHub Pages requires public repositories unless you have a Pro account)
6. Click "Create repository"

## Step 2: Push Your Code to GitHub

From your local project directory, run:

```bash
# Initialize a new Git repository (if not already done)
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial website commit"

# Add the remote repository URL
git remote add origin https://github.com/yourusername/RDwebsite.git

# Push to GitHub
git push -u origin main
```

## Step 3: Configure GitHub Pages

1. Go to your repository on GitHub
2. Click on "Settings"
3. Scroll down to the "GitHub Pages" section
4. Under "Source", select the branch you want to deploy (usually `main`)
5. Click "Save"

## Step 4: Custom Domain Configuration

### In GitHub:

1. In the GitHub Pages section of your repository settings
2. Enter your custom domain (e.g., `yourdomain.com` or `www.yourdomain.com`) in the "Custom domain" field
3. Click "Save"
4. Check the "Enforce HTTPS" option (recommended for security)

### In Dynadot:

1. Log in to your Dynadot account
2. Navigate to your domain's DNS management page
3. Set up the following DNS records:

   **For apex domain (yourdomain.com):**
   
   Add these A records pointing to GitHub Pages IP addresses:
   ```
   Type: A
   Host: @
   Value: 185.199.108.153
   TTL: 600 or Auto
   
   Type: A
   Host: @
   Value: 185.199.109.153
   TTL: 600 or Auto
   
   Type: A
   Host: @
   Value: 185.199.110.153
   TTL: 600 or Auto
   
   Type: A
   Host: @
   Value: 185.199.111.153
   TTL: 600 or Auto
   ```
   
   **For www subdomain:**
   ```
   Type: CNAME
   Host: www
   Value: yourusername.github.io.
   TTL: 600 or Auto
   ```

4. Save your DNS settings

## Step 5: Verify Domain Setup

1. The CNAME file in your repository should contain your custom domain (e.g., `www.yourdomain.com` or `yourdomain.com`)
2. Ensure the `.nojekyll` file exists in your repository to prevent GitHub's Jekyll processing
3. Wait for DNS propagation (this can take anywhere from a few minutes to 48 hours)

## Step 6: Test Your Site

1. After DNS propagation is complete, visit your custom domain in a browser
2. Verify that your website loads correctly
3. Check that HTTPS is working (look for the padlock icon in your browser)

## Troubleshooting

If your site doesn't work as expected, check the following:

- **404 Error**: Make sure your repository contains an index.html file at the root level
- **DNS Issues**: Verify that your DNS records match GitHub's requirements
- **Custom Domain Not Working**: Ensure your CNAME file contains the correct domain
- **HTTPS Not Working**: It can take up to 24 hours for GitHub to provision SSL certificates

## Maintaining Your Site

To update your website:

1. Make changes to your local files
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```
3. GitHub Pages will automatically rebuild and deploy your site

## Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Pages Custom Domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [Troubleshooting Custom Domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages)
