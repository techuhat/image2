# Project Structure - ImagePDF Toolkit

## 📁 New Organized Structure

```
d:\toolkit-main/
├── 📄 index.html                 # Main GitHub Pages entry point (ROOT)
├── 📄 README.md                  # Project documentation
├── 📄 CNAME                      # GitHub Pages custom domain
├── 
├── 📁 src/                       # Source code
│   ├── 📁 frontend/              # Frontend code
│   │   ├── 📁 pages/             # Web pages
│   │   │   ├── index.html        # Copy of main page
│   │   │   ├── about.html        # About page
│   │   │   ├── contact.html      # Contact page
│   │   │   ├── privacy.html      # Privacy policy
│   │   │   └── terms.html        # Terms of service
│   │   │
│   │   └── 📁 tools/             # Tools organized by category
│   │       ├── 📁 pdf-tools/     # PDF-related tools
│   │       │   ├── pdf-to-doc.html
│   │       │   ├── pdf-to-images.html
│   │       │   └── pdf-compressor.html
│   │       │
│   │       ├── 📁 image-tools/   # Image-related tools
│   │       │   ├── image-to-pdf.html
│   │       │   ├── image-compressor.html
│   │       │   ├── image-resizer.html
│   │       │   └── format-converter.html
│   │       │
│   │       └── 📁 utility-tools/ # Utility tools
│   │           ├── batch-processor.html
│   │           └── qr-generator.html
│   │
│   └── 📁 backend/               # Backend Flask application
│       ├── app.py                # Main Flask app
│       ├── run.py                # Development runner
│       ├── startup.py            # Azure startup script
│       └── requirements.txt      # Python dependencies
│
├── 📁 public/                    # Static assets (GitHub Pages accessible)
│   ├── 📁 css/                   # Stylesheets
│   │   ├── all.min.css
│   │   └── premium-buttons.css
│   │
│   ├── 📁 js/                    # JavaScript files
│   │   ├── backend-config.js
│   │   ├── jspdf.min.js
│   │   └── lib/
│   │
│   ├── 📁 images/                # Images
│   │   └── og.png
│   │
│   ├── 📁 assets/                # Other assets
│   │   └── svg-icons/
│   │
│   ├── script.js                 # Main JavaScript
│   ├── styles.min.css            # Main CSS
│   ├── tailwind-complete.css     # Tailwind CSS
│   ├── manifest.json             # PWA manifest
│   ├── service-worker.js         # Service worker
│   ├── robots.txt                # SEO robots file
│   └── sitemap.xml               # SEO sitemap
│
├── 📁 deployment/                # Deployment files
│   ├── deploy-azure.ps1          # Azure deployment script
│   └── Dockerfile                # Docker configuration
│
├── 📁 docs/                      # Documentation
│   ├── AZURE_DEPLOYMENT.md
│   ├── AZURE_MIGRATION_COMPLETE.md
│   ├── AZURE_SETUP_COMPLETE.md
│   ├── DEPLOYMENT_SUMMARY.md
│   └── CLEANUP_SUMMARY.md
│
├── 📁 cache/                     # Temporary cache
├── 📁 temp/                      # Temporary files
└── 📁 backend-env/               # Python virtual environment
```

## 🎯 Benefits of New Structure

### ✅ **Organized by Features**
- **PDF Tools**: All PDF-related functionality in one place
- **Image Tools**: All image processing tools together  
- **Utility Tools**: General purpose tools like QR generator, batch processor

### ✅ **GitHub Pages Compatible**
- **index.html in root**: GitHub Pages automatically serves from root
- **Public assets**: All static files in `/public/` folder
- **SEO optimized**: robots.txt, sitemap.xml in public folder

### ✅ **Development Friendly**
- **Separate frontend/backend**: Clear separation of concerns
- **Deployment scripts**: All deployment files in `/deployment/`
- **Documentation**: All docs in `/docs/` folder

### ✅ **Scalable Architecture**
- **Modular structure**: Easy to add new tools
- **Category-based**: Tools grouped by functionality
- **Clean separation**: Source code vs public assets

## 🔗 Updated Links

All links in index.html have been updated to reflect the new structure:

- **Tool Links**: `src/frontend/tools/{category}/{tool}.html`
- **Page Links**: `src/frontend/pages/{page}.html`  
- **Asset Links**: `public/{asset}`
- **CSS/JS**: `public/css/` and `public/js/`

## 🚀 Ready for GitHub Pages

The structure is now optimized for GitHub Pages deployment with proper organization and maintainability.
