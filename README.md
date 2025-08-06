# 🛠️ ImagePDF Toolkit

A comprehensive, privacy-focused toolkit for image and PDF processing. All operations are performed client-side in your browser for complete privacy and security.

## 🌟 Features

- **100% Client-Side Processing** - Your files never leave your device
- **No Server Uploads Required** - Everything happens in your browser
- **Multi-Format Support** - Images (JPEG, PNG, WebP, AVIF, BMP, TIFF) and PDFs
- **Batch Processing** - Handle multiple files simultaneously
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark Mode Support** - Switch between light and dark themes
- **Progressive Web App** - Install as a native app

## � Available Tools

### 📄 PDF Tools
- **[Image to PDF](tools/image-to-pdf.html)** - Convert multiple images into a single PDF
- **[PDF to Images](tools/pdf-to-images.html)** - Extract images from PDF files
- **[PDF to DOC](tools/pdf-to-doc.html)** - Convert PDF files to Word documents

### 🖼️ Image Tools
- **[Image Compressor](tools/image-compressor.html)** - Reduce image file sizes while maintaining quality
- **[Image Resizer](tools/image-resizer.html)** - Resize images with custom dimensions
- **[Format Converter](tools/format-converter.html)** - Convert between different image formats
- **[Batch Processor](tools/batch-processor.html)** - Apply multiple operations (resize, compress, convert) in one go

### 🔤 Utility Tools
- **[QR Generator](tools/qr-generator.html)** - Generate QR codes for text, URLs, and more

## 🚀 Getting Started

### Online Access
Visit the live toolkit at: `https://yourusername.github.io/image2/`

### Local Installation
1. Clone or download this repository
2. Open `index.html` in any modern web browser
3. Start using the tools immediately

### PWA Installation
1. Visit the toolkit in a compatible browser
2. Look for the "Install App" prompt or use browser menu
3. Install as a Progressive Web App for offline access

## 💻 Technical Details

### Browser Requirements
- Modern browsers with JavaScript enabled
- HTML5 Canvas support
- File API support
- Blob API support

### File Size Limits
- Limited only by your device's available memory
- Recommended maximum: 50MB per file for optimal performance

### Supported Formats

#### Images (Input/Output)
- JPEG/JPG
- PNG
- WebP
- AVIF
- BMP
- TIFF

#### PDF (Input/Output)
- PDF (Portable Document Format)
- DOC (Microsoft Word Document)

### Local Dependencies for Offline Use
- The toolkit requires `pdf.min.js` and `pdf.worker.min.js` from PDF.js library for PDF processing.
- These files are included locally in the `js/` directory to ensure full offline compatibility.
- No external CDN dependencies are used for PDF processing.

## 🔒 Privacy & Security

- **No Server Communication** - All processing happens locally
- **No File Uploads** - Files are processed directly in your browser
- **No Data Collection** - No analytics, tracking, or data harvesting
- **Client-Side Only** - No backend servers involved
- **Secure by Design** - Files never leave your device

## 🏗️ Architecture

### Frontend Stack
- **HTML5** with semantic markup
- **CSS3** with Tailwind CSS framework
- **Vanilla JavaScript** for all functionality
- **Service Worker** for PWA capabilities

### File Structure
```
├── index.html              # Main landing page
├── tools/                  # Individual tool pages
│   ├── image-to-pdf.html
│   ├── pdf-to-images.html
│   ├── image-compressor.html
│   ├── image-resizer.html
│   ├── format-converter.html
│   ├── batch-processor.html
│   ├── pdf-to-doc.html
│   └── qr-generator.html
├── script.js               # Main JavaScript functionality
├── styles.min.css          # Custom styles
├── tailwind-complete.css   # Tailwind CSS framework
├── css/                    # Additional stylesheets
├── assets/                 # Static assets
│   └── svg-icons/          # Tool icons
└── manifest.json           # PWA manifest
```

### JavaScript Architecture
The main `script.js` file is organized into clearly commented sections:

```javascript
// ================================================================================
// [Start] SHARED UTILITIES AND HELPERS
// ================================================================================

// ================================================================================
// [Start] CORE IMAGE PROCESSING FUNCTIONS
// ================================================================================

// ================================================================================
// [Start] IMAGE COMPRESSOR TOOL
// ================================================================================

// ================================================================================
// [Start] IMAGE TO PDF TOOL
// ================================================================================

// ================================================================================
// [Start] PDF TO IMAGES TOOL
// ================================================================================

// ================================================================================
// [Start] IMAGE RESIZER TOOL
// ================================================================================

// ================================================================================
// [Start] FORMAT CONVERTER TOOL
// ================================================================================

// ================================================================================
// [Start] BATCH PROCESSOR TOOL
// ================================================================================
```

## 🛠️ Development

### Adding New Tools
1. Create a new HTML file in the `tools/` directory
2. Follow the existing pattern with proper SEO meta tags
3. Add the tool functionality to `script.js` in a new commented section
4. Update navigation links in `index.html`

### Code Standards
- Use semantic HTML5
- Follow established CSS class patterns
- Comment all JavaScript functions
- Maintain responsive design principles
- Ensure accessibility compliance

## 📱 Mobile Support

- Responsive design adapts to all screen sizes
- Touch-friendly interface elements
- Optimized file handling for mobile devices
- PWA capabilities for app-like experience

## ⚡ Performance

- Optimized image processing algorithms
- Efficient memory management
- Progressive loading of large files
- Compression quality optimization
- Batch processing with progress feedback

## 🔄 Updates & Versioning

### Current Version: 2.0

#### Version 2.0 Features:
- Individual tool pages for better navigation
- Improved batch processing capabilities
- Enhanced mobile responsiveness
- Advanced compression algorithms
- Better error handling and user feedback

### Update History:
- **v2.0** - Individual tool pages, enhanced functionality
- **v1.0** - Initial release with modal-based interface

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make changes following the code standards
4. Test thoroughly across different browsers
5. Submit a pull request with detailed description

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with ❤️ by [Tech U](https://github.com/techuhat)
- Icons and assets from various open source projects
- Tailwind CSS for the design framework

## 📞 Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check the documentation
- Review existing issues for solutions

---

**Made with ❤️ for the community • Privacy-First • No Tracking • Completely Free**
│   └── shared.js            # Shared utilities
├── tools/                    # Individual tool pages
│   ├── pdf-to-doc.html      # PDF to DOC converter
│   └── qr-generator.html    # QR code generator
├── assets/
│   └── svg-icons/           # Local SVG icons
│       ├── pdf-icon.svg
│       ├── image-icon.svg
│       ├── qr-icon.svg
│       ├── compress-icon.svg
│       ├── color-icon.svg
│       ├── text-icon.svg
│       └── batch-icon.svg
└── images/
    └── og.png               # Open Graph image
```

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/image2.git
   cd image2
   ```

2. **Serve locally** (any static server)
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js
   npx serve .
   
   # Using PHP
   php -S localhost:8000
   ```

3. **Open in browser**
   ```
   http://localhost:8000
   ```

## 📱 PWA Installation

The toolkit is a Progressive Web App (PWA) that can be installed on:
- **Desktop**: Chrome, Edge, Firefox
- **Mobile**: iOS Safari, Android Chrome
- **Tablet**: All modern browsers

Installation prompts will appear automatically, or users can:
- **Desktop**: Click the install icon in the address bar
- **Mobile**: Add to home screen from browser menu

## 🎨 Design System

### Color Palette
- **Primary**: Blue (#4F46E5)
- **Secondary**: Purple (#7C3AED)
- **Success**: Green (#10B981)
- **Warning**: Orange (#F59E0B)
- **Error**: Red (#EF4444)

### Typography
- **Font**: System fonts (ui-sans-serif)
- **Headings**: Bold weights (700)
- **Body**: Regular weights (400-500)

### Components
- **Cards**: Rounded corners (12px), subtle shadows
- **Buttons**: Gradient backgrounds, hover animations
- **Forms**: Consistent styling with focus states
- **Modals**: Backdrop blur, smooth animations

## 🔧 Development

### Adding New Tools

1. **Create tool page** in `tools/` directory
2. **Add tool card** to `index.html`
3. **Update navigation** in footer
4. **Add to service worker** cache list
5. **Update manifest** shortcuts

### Tool Page Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- SEO Meta Tags -->
    <title>Tool Name - Description | ImagePDF Toolkit</title>
    <meta name="description" content="Tool description">
    
    <!-- Stylesheets -->
    <link rel="stylesheet" href="../styles.min.css">
    <link rel="stylesheet" href="../tailwind-complete.css">
</head>
<body>
    <!-- Navigation -->
    <nav>...</nav>
    
    <!-- Main Content -->
    <main>
        <!-- Tool Header -->
        <!-- Tool Interface -->
        <!-- Results Section -->
    </main>
    
    <!-- Scripts -->
    <script src="../js/shared.js"></script>
    <script>
        // Tool-specific logic
    </script>
</body>
</html>
```

## 📊 Performance

### PageSpeed Insights Targets
- **Mobile**: 95+ score
- **Desktop**: 95+ score

### Optimization Techniques
- **Minified CSS/JS** - Reduced file sizes
- **Local assets** - No external dependencies
- **Lazy loading** - Images and components
- **Service worker** - Caching strategy
- **Compressed images** - WebP format where possible

## 🔒 Privacy & Security

- **No data collection** - All processing is client-side
- **No analytics** - Privacy-first approach
- **No tracking** - No cookies or external scripts
- **Open source** - Transparent codebase

## 🌐 Browser Support

- **Chrome**: 88+
- **Firefox**: 85+
- **Safari**: 14+
- **Edge**: 88+
- **Mobile browsers**: iOS 14+, Android 10+

## 📈 SEO Features

### Each tool page includes:
- **Unique title tags** - Descriptive and keyword-rich
- **Meta descriptions** - Compelling summaries
- **Open Graph tags** - Social media optimization
- **Structured data** - JSON-LD schema markup
- **Canonical URLs** - Prevent duplicate content
- **H1/H2 tags** - Proper heading hierarchy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Tailwind CSS** - Utility-first CSS framework
- **PDF.js** - PDF processing library
- **jsPDF** - PDF generation library
- **Canvas API** - Image processing capabilities

## 📞 Support

- **GitHub Issues**: [Report bugs](https://github.com/yourusername/image2/issues)
- **Email**: [Contact support](mailto:support@techuhat.com)
- **Documentation**: [Wiki](https://github.com/yourusername/image2/wiki)

---

**Built with ❤️ by TechUhat** 