# PDF to DOC Backend Server

Advanced backend service for PDF to DOC conversion with OCR, image extraction, and formatting preservation.

## Features

### 🚀 **Advanced PDF Processing**
- **High-Quality Text Extraction** - Better than client-side processing
- **Image Detection & Extraction** - Preserve images separately
- **OCR Support** - Convert scanned PDFs to editable text
- **Format Preservation** - Maintain layouts, tables, and styling
- **Multiple Output Formats** - DOC, DOCX, RTF support

### 🔧 **Technical Capabilities**
- **LibreOffice Integration** - Professional-grade conversion
- **Fallback Systems** - Multiple conversion methods
- **File Management** - Automatic cleanup and download
- **Error Handling** - Robust error recovery
- **CORS Support** - Frontend integration ready

## Quick Start

### 1. Install Dependencies
```bash
cd backend-example
npm install
```

### 2. Optional: Install LibreOffice (Recommended)
```bash
# Ubuntu/Debian
sudo apt-get install libreoffice

# macOS
brew install --cask libreoffice

# Windows
# Download from https://www.libreoffice.org/download/
```

### 3. Start Server
```bash
npm start
# Server runs on http://localhost:3001
```

### 4. Development Mode
```bash
npm run dev  # Auto-restart on changes
```

## API Endpoints

### Health Check
```http
GET /health
```

### Convert PDF to DOC
```http
POST /api/pdf-to-doc/convert
Content-Type: multipart/form-data

Body:
- file: PDF file (max 100MB)
- outputFormat: "docx" | "doc" | "rtf" (optional, default: "docx")
- preserveImages: "true" | "false" (optional, default: "true")
- enableOCR: "true" | "false" (optional, default: "true")
```

### Download Converted File
```http
GET /api/pdf-to-doc/download/:filename
```

## Frontend Integration

Update your frontend's backend configuration:

```javascript
const BACKEND_CONFIG = {
    baseUrl: 'http://localhost:3001', // Your server URL
    endpoints: {
        convert: '/api/pdf-to-doc/convert',
        download: '/api/pdf-to-doc/download'
    }
};
```

## Production Setup

### 1. Environment Variables
```bash
PORT=3001
NODE_ENV=production
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=104857600  # 100MB
```

### 2. PM2 Process Manager
```bash
npm install -g pm2
pm2 start server.js --name pdf-converter
pm2 save
pm2 startup
```

### 3. Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /api/pdf-to-doc/ {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        client_max_body_size 100M;
    }
}
```

## Advanced Features Setup

### 1. OCR with Tesseract
```bash
# Install Tesseract OCR
sudo apt-get install tesseract-ocr
npm install tesseract.js
```

### 2. Image Processing
```bash
npm install sharp pdf2pic
```

### 3. Advanced PDF Parsing
```bash
npm install pdf-parse pdf2json
```

## Performance Optimization

### 1. File Cleanup
- Automatic file deletion after download
- Configurable cleanup intervals
- Storage monitoring

### 2. Processing Queue
```javascript
// Add queue system for heavy processing
npm install bull redis
```

### 3. Caching
```javascript
// Cache processed results
npm install redis node-cache
```

## Security Considerations

### 1. File Validation
- MIME type checking
- File size limits
- Virus scanning (optional)

### 2. Rate Limiting
```javascript
npm install express-rate-limit
```

### 3. HTTPS Setup
```javascript
// Use HTTPS in production
const https = require('https');
```

## Monitoring & Logging

### 1. Request Logging
```javascript
npm install morgan winston
```

### 2. Health Monitoring
```javascript
npm install express-healthcheck
```

## Troubleshooting

### Common Issues

1. **LibreOffice Not Found**
   ```bash
   which libreoffice
   # Add to PATH if needed
   ```

2. **Permission Errors**
   ```bash
   chmod +x node_modules/.bin/libreoffice
   ```

3. **Memory Issues**
   ```bash
   node --max-old-space-size=4096 server.js
   ```

## API Response Examples

### Successful Conversion
```json
{
  "success": true,
  "jobId": "job_1691234567890_abc123",
  "downloadUrl": "/api/pdf-to-doc/download/converted-file.docx",
  "originalName": "document.pdf",
  "convertedName": "document.docx",
  "features": {
    "textExtracted": true,
    "imagesExtracted": true,
    "imageCount": 3,
    "ocrApplied": false,
    "formatting": "advanced"
  }
}
```

### Error Response
```json
{
  "error": "Conversion failed",
  "message": "Unsupported PDF format"
}
```

## License

MIT License - feel free to use in your projects!

## Support

For issues and feature requests, please create an issue in the main repository.
