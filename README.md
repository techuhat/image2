# PDF Tools Toolkit - Azure App Service

A complete web-based toolkit for PDF and image processing with Azure App Service backend.

## 🎉 Azure Deployment Status: COMPLETE ✅

Your Azure App Service is ready:
- **App Name**: imagetool
- **Resource Group**: imagetool_group
- **Subscription**: Azure for Students
- **Plan**: B1 (Basic)
- **Python Version**: 3.10
- **App URL**: https://imagetool-h4dmewahfmg4bkej.eastasia-01.azurewebsites.net

## 🚀 Features

### Client-Side Tools (No Server Required)
- **Image to PDF** - Convert multiple images into a single PDF
- **PDF to Images** - Extract images from PDF files
- **Image Compressor** - Reduce file sizes while maintaining quality
- **Image Resizer** - Resize images with custom dimensions
- **Format Converter** - Convert between different image formats
- **QR Generator** - Generate QR codes for text, URLs, and more
- **Batch Processor** - Apply multiple operations in sequence

### Server-Side Processing (Azure Backend) - SmallPDF/iLovePDF Level
- **PDF to DOCX Converter** - Enhanced server-side conversion with OCR support
- **PDF Compressor** - Advanced compression using Azure resources
- **PDF OCR** - Extract text from scanned PDFs using Tesseract/EasyOCR
- **PDF Merge** - Combine multiple PDFs into one
- **PDF Split** - Split PDFs by pages or ranges
- **PDF Rotate** - Rotate PDF pages
- **PDF Protect/Unlock** - Password protection and removal
- **Batch Processing** - Process multiple files simultaneously
- **File Caching** - Avoid redundant processing
- **Health Monitoring** - Built-in health checks
- **Advanced Processing** - Multi-language OCR, advanced compression
- **Real-time Processing** - Fast response times with cloud infrastructure

## 📦 Quick Deployment

### Step 1: Deploy Your Code
```powershell
# Run this PowerShell command
.\deploy-azure.ps1 -ResourceGroupName "imagetool_group" -AppName "imagetool"
```

### Step 2: Test Your Backend
```bash
# Test endpoints
curl https://imagetool-h4dmewahfmg4bkej.eastasia-01.azurewebsites.net/health
curl https://imagetool-h4dmewahfmg4bkej.eastasia-01.azurewebsites.net/ping
```

## 🎯 Azure Benefits

### ✅ **Cost-Effective**
- Free with Azure for Students
- B1 plan perfect for development
- Pay only for actual usage

### ✅ **Scalable & Reliable**
- Auto-scaling capabilities
- 99.95% uptime SLA
- Global CDN integration

### ✅ **Secure**
- HTTPS by default
- Azure security features
- Built-in DDoS protection

### ✅ **Easy Management**
- Azure Portal integration
- One-click scaling
- Integrated monitoring

## 🔧 Project Structure

```
├── 📄 index.html                 # Main GitHub Pages entry point
├── 📁 src/                       # Source code
│   ├── 📁 frontend/              # Frontend application
│   │   ├── 📁 pages/             # Web pages
│   │   └── 📁 tools/             # Tools by category
│   │       ├── 📁 pdf-tools/     # PDF processing tools
│   │       ├── 📁 image-tools/   # Image processing tools
│   │       └── 📁 utility-tools/ # Utility tools
│   └── 📁 backend/               # Flask backend (Azure)
│
├── 📁 public/                    # Static assets
│   ├── 📁 css/, js/, images/     # Stylesheets, scripts, images
│   └── manifest.json, robots.txt # PWA & SEO files
│
├── � deployment/                # Azure deployment scripts
└── 📁 docs/                      # Project documentation
```

## 🧪 Testing Your Deployment

After deployment, your endpoints will be:
- **Health Check**: https://imagetool-h4dmewahfmg4bkej.eastasia-01.azurewebsites.net/health
- **Ping Test**: https://imagetool-h4dmewahfmg4bkej.eastasia-01.azurewebsites.net/ping
- **PDF to DOCX**: https://imagetool-h4dmewahfmg4bkej.eastasia-01.azurewebsites.net/pdf-to-docx

## 📱 Frontend Integration

Your frontend automatically connects to Azure backend:
```javascript
// Backend configured in js/backend-config.js
baseUrl: 'https://imagetool-h4dmewahfmg4bkej.eastasia-01.azurewebsites.net'
```

## 📦 Backend Dependencies

These advanced libraries are required for SmallPDF/iLovePDF level functionality and are already listed in `requirements.txt`:

### Core PDF Processing
- pdf2docx - PDF to DOCX conversion
- PyMuPDF (fitz) - Advanced PDF manipulation
- python-docx - DOCX document creation

### Advanced PDF Features
- pikepdf - Modern PDF processing
- pdfplumber - PDF text extraction
- pytesseract - OCR text recognition
- easyocr - Multi-language OCR
- opencv-python - Image processing
- numpy - Numerical computing

### Document Processing
- openpyxl - Excel file processing
- xlrd - Excel file reading
- python-pptx - PowerPoint processing

### Performance & Security
- cryptography - File encryption
- redis - Caching (optional)
- celery - Background processing (optional)

Install all dependencies with:

```bash
pip install -r requirements.txt
```

**Note:** For OCR functionality, you may also need to install Tesseract OCR system:
- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **Linux**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`

## 🏗️ Architecture

### Client-Side Processing
- **Instant**: No uploads required
- **Private**: Files never leave browser
- **Offline**: Works without internet

### Server-Side Processing (Azure)
- **Advanced**: Better quality conversion
- **Scalable**: Handles large files
- **Reliable**: Cloud infrastructure

## 📊 Monitoring

Azure provides built-in monitoring:
- **Application Insights** - Performance metrics
- **Log Analytics** - Real-time logs
- **Alerts** - Automated notifications
- **Scaling** - Auto-scale rules

## 🎉 Ready to Go!

Your Azure setup is complete. Just run the deployment script and your PDF tools will be live with both client-side and server-side processing capabilities!

**Next Command**: `.\deploy-azure.ps1 -ResourceGroupName "imagetool_group" -AppName "imagetool"`