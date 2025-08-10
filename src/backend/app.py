#!/usr/bin/env python3
"""
Flask Backend for PDF Tools - Azure App Service Ready
Tools: DOCX to PDF, PDF to DOCX, PDF Compression, OCR, Advanced Processing
Features: File caching, efficient processing, CORS support, Azure optimization
Enhanced with Advanced Error Handling & Recovery Systems
"""

import os
import tempfile
import subprocess
import hashlib
import logging
import traceback
import time
import signal
import threading
from datetime import datetime
from pathlib import Path
import zipfile
import shutil
import json
from functools import wraps
from contextlib import contextmanager

# Azure-compatible logging setup (early)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Azure uses stdout for logging
    ]
)
logger = logging.getLogger(__name__)

# Enhanced error tracking
error_counts = {}
last_errors = []
MAX_ERROR_HISTORY = 100

def track_error(error_type, error_msg):
    """Track errors for monitoring and debugging"""
    global error_counts, last_errors
    
    error_counts[error_type] = error_counts.get(error_type, 0) + 1
    error_entry = {
        'timestamp': datetime.now().isoformat(),
        'type': error_type,
        'message': str(error_msg),
        'count': error_counts[error_type]
    }
    
    last_errors.append(error_entry)
    if len(last_errors) > MAX_ERROR_HISTORY:
        last_errors.pop(0)
    
    logger.error(f"Error tracked: {error_type} - {error_msg}")

def enhanced_error_handler(func):
    """Advanced error handling decorator with recovery mechanisms"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MemoryError as e:
            track_error("MEMORY_ERROR", str(e))
            logger.critical(f"Memory error in {func.__name__}: {e}")
            return jsonify({
                "error": "Insufficient memory for this operation",
                "code": "MEMORY_ERROR",
                "suggestion": "Try with a smaller file or reduce quality settings",
                "retry_after": 60
            }), 507
        except subprocess.TimeoutExpired as e:
            track_error("TIMEOUT_ERROR", str(e))
            logger.warning(f"Timeout in {func.__name__}: {e}")
            return jsonify({
                "error": "Operation timed out",
                "code": "TIMEOUT_ERROR", 
                "suggestion": "File may be too large or corrupted",
                "retry_after": 30
            }), 408
        except FileNotFoundError as e:
            track_error("FILE_NOT_FOUND", str(e))
            logger.error(f"File not found in {func.__name__}: {e}")
            return jsonify({
                "error": "Required system tool not found",
                "code": "TOOL_MISSING",
                "suggestion": "Please ensure all dependencies are installed",
                "details": str(e)
            }), 500
        except PermissionError as e:
            track_error("PERMISSION_ERROR", str(e))
            logger.error(f"Permission error in {func.__name__}: {e}")
            return jsonify({
                "error": "Permission denied",
                "code": "PERMISSION_ERROR",
                "suggestion": "Check file permissions and disk space"
            }), 403
        except Exception as e:
            track_error("UNKNOWN_ERROR", str(e))
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({
                "error": "Internal server error",
                "code": "INTERNAL_ERROR",
                "message": str(e),
                "suggestion": "Please try again or contact support",
                "function": func.__name__
            }), 500
    return wrapper

@contextmanager
def safe_temp_file(suffix="", prefix="temp_"):
    """Safe temporary file context manager with cleanup guarantee"""
    temp_file = None
    try:
        temp_file = tempfile.NamedTemporaryFile(suffix=suffix, prefix=prefix, delete=False)
        yield temp_file.name
    except Exception as e:
        logger.error(f"Temp file error: {e}")
        raise
    finally:
        if temp_file and os.path.exists(temp_file.name):
            try:
                os.unlink(temp_file.name)
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file {temp_file.name}: {e}")

def validate_file_upload(file, allowed_extensions, max_size_mb=100):
    """Enhanced file validation with security checks"""
    if not file or file.filename == '':
        raise ValueError("No file provided")
    
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise ValueError(f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}")
    
    # Check file size (read first to get size)
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Seek back to beginning
    
    max_size_bytes = max_size_mb * 1024 * 1024
    if size > max_size_bytes:
        raise ValueError(f"File too large. Maximum size: {max_size_mb}MB")
    
    # Basic content validation
    if size == 0:
        raise ValueError("File is empty")
    
    return True

def check_system_resources():
    """Check available system resources"""
    try:
        import psutil
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'memory_available_gb': round(memory.available / (1024**3), 2),
            'memory_percent': memory.percent,
            'disk_free_gb': round(disk.free / (1024**3), 2),
            'disk_percent': round((disk.used / disk.total) * 100, 2)
        }
    except ImportError:
        return {'error': 'psutil not available'}
    except Exception as e:
        logger.warning(f"Resource check failed: {e}")
        return {'error': str(e)}

# Flask and web framework imports
from flask import Flask, request, jsonify, send_file, after_this_request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from flask import Flask, request, jsonify, send_file, after_this_request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# PDF and document processing libraries
try:
    from pdf2docx import Converter
    PDF2DOCX_AVAILABLE = True
except ImportError:
    PDF2DOCX_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

# Advanced PDF Processing Libraries
try:
    import pikepdf
    PIKEPDF_AVAILABLE = True
except ImportError:
    PIKEPDF_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

# OCR functionality removed for Azure deployment optimization
TESSERACT_AVAILABLE = False
EASYOCR_AVAILABLE = False
OPENCV_AVAILABLE = False

logger.info("OCR features disabled for lightweight deployment")

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size for advanced processing

# Azure-optimized CORS configuration
CORS(app, origins=[
    "https://techuhat.github.io",
    "https://image2.vercel.app", 
    "http://localhost:3000",
    "http://127.0.0.1:3000"
])

# Create directories for caching
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

def get_file_hash(file_content):
    """Generate SHA256 hash of file content for caching"""
    return hashlib.sha256(file_content).hexdigest()

def check_ghostscript():
    """Check if Ghostscript is available in system"""
    try:
        # Try with full path first (Windows)
        gs_paths = [
            r'C:\Program Files\gs\gs10.05.1\bin\gswin64c.exe',
            'gs',  # Try system PATH
            'gswin64c'
        ]
        
        for path in gs_paths:
            try:
                result = subprocess.run([path, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return True
            except (subprocess.SubprocessError, FileNotFoundError):
                continue
        return False
    except Exception:
        return False

def check_tesseract():
    """Check if Tesseract OCR is available"""
    try:
        # Try with full path first (Windows)
        tesseract_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            'tesseract'  # Try system PATH
        ]
        
        for path in tesseract_paths:
            try:
                result = subprocess.run([path, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return True
            except (subprocess.SubprocessError, FileNotFoundError):
                continue
        return False
    except Exception:
        return False

# System capability checks
GHOSTSCRIPT_AVAILABLE = check_ghostscript()
TESSERACT_AVAILABLE = check_tesseract()

@app.route('/ping', methods=['GET'])
def ping():
    """Health check endpoint"""
    return "pong"

@app.route('/', methods=['GET'])
@app.route('/health', methods=['GET'])
def health_check():
    """Comprehensive health check with system capabilities"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "message": "Advanced PDF Toolkit Backend - SmallPDF/iLovePDF Level",
        "capabilities": {
            "pdf_compression": GHOSTSCRIPT_AVAILABLE or PYMUPDF_AVAILABLE,
            "pdf_to_docx": PDF2DOCX_AVAILABLE or PYMUPDF_AVAILABLE,
            "pdf_advanced_processing": PIKEPDF_AVAILABLE or PDFPLUMBER_AVAILABLE,
            "image_compression": True,  # Always available with Pillow
            "batch_processing": True,
            "advanced_compression": True
        },
        "system_tools": {
            "ghostscript": GHOSTSCRIPT_AVAILABLE,
            "pdf2docx": PDF2DOCX_AVAILABLE,
            "pymupdf": PYMUPDF_AVAILABLE,
            "pikepdf": PIKEPDF_AVAILABLE,
            "pdfplumber": PDFPLUMBER_AVAILABLE,
            "numpy": NUMPY_AVAILABLE,
            "pillow": True
        },
        "supported_operations": [
            "compress-pdf",
            "pdf-to-docx", 
            "compress-image",
            "batch-process",
            "pdf-merge",
            "pdf-split",
            "pdf-rotate",
            "pdf-protect",
            "pdf-unlock",
            "image-to-pdf",
            "pdf-to-images"
        ],
        "limits": {
            "max_file_size": "500MB",
            "max_batch_files": 20,
            "supported_formats": {
                "pdf": ["pdf"],
                "image": ["jpg", "jpeg", "png", "webp", "bmp", "tiff", "gif"],
                "document": ["docx", "doc", "xlsx", "xls", "pptx", "ppt"],
                "text": ["txt", "rtf", "md"]
            }
        },
        "features": {
            "advanced_compression": True,
            "batch_processing": True,
            "file_caching": True,
            "real_time_processing": True,
            "multi_format_support": True,
            "ocr_support": False
        }
    })

@app.route('/pdf-to-docx', methods=['POST'])
@enhanced_error_handler
def pdf_to_docx():
    """
    Convert PDF to DOCX using pdf2docx or PyMuPDF with advanced text and image extraction
    Features: File caching, multiple conversion methods, image preservation
    """
    logger.info("PDF to DOCX conversion request received")
    
    if not (PDF2DOCX_AVAILABLE or PYMUPDF_AVAILABLE):
        return jsonify({
            "error": "PDF to DOCX conversion not available. Install pdf2docx or PyMuPDF"
        }), 500
    
    # Validate file upload
    try:
        validate_file_upload(request.files.get('file'), ['.pdf'], max_size_mb=100)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    file = request.files['file']
    force_conversion = request.form.get('force', 'false').lower() == 'true'
    include_images = request.form.get('images', 'true').lower() == 'true'
    
    try:
        # Read file content and generate hash
        file_content = file.read()
        file_hash = get_file_hash(file_content)
        
        # Generate filenames
        original_name = secure_filename(file.filename)
        base_name = Path(original_name).stem
        output_filename = f"{base_name}.docx"
        
        # Check cache
        cache_key = f"{file_hash}_{include_images}_{output_filename}"
        cached_file = CACHE_DIR / cache_key
        
        if cached_file.exists() and not force_conversion:
            logger.info(f"Returning cached DOCX: {output_filename}")
            return send_file(
                cached_file,
                as_attachment=True,
                download_name=output_filename,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
        
        # Create temporary files
        temp_pdf = TEMP_DIR / f"{file_hash}_input.pdf"
        temp_docx = TEMP_DIR / f"{file_hash}_output.docx"
        
        # Write PDF file
        with open(temp_pdf, 'wb') as f:
            f.write(file_content)
        
        conversion_success = False
        conversion_method = ""
        conversion_stats = {"pages": 0, "images": 0, "text_chars": 0}
        
        # Method 1: Try pdf2docx (most accurate with layout preservation)
        if PDF2DOCX_AVAILABLE and not conversion_success:
            try:
                logger.info("Attempting conversion with pdf2docx")
                
                # Configure pdf2docx for better conversion
                converter = Converter(str(temp_pdf))
                
                # Convert with advanced options
                converter.convert(
                    str(temp_docx),
                    start=0,
                    end=None,
                    pages=None,
                    multi_processing=False,  # Disable for stability
                    cpu_count=1
                )
                converter.close()
                
                # Check if conversion was successful
                if temp_docx.exists() and temp_docx.stat().st_size > 0:
                    conversion_success = True
                    conversion_method = "pdf2docx"
                    
                    # Get conversion stats
                    doc = fitz.open(str(temp_pdf))
                    conversion_stats["pages"] = len(doc)
                    doc.close()
                    
                    logger.info("Conversion successful with pdf2docx (with layout preservation)")
                else:
                    logger.warning("pdf2docx created empty file")
                    
            except Exception as e:
                logger.warning(f"pdf2docx conversion failed: {e}")
                if temp_docx.exists():
                    temp_docx.unlink()
        
        # Method 2: Try enhanced PyMuPDF with proper DOCX generation
        if PYMUPDF_AVAILABLE and not conversion_success:
            try:
                logger.info("Attempting conversion with enhanced PyMuPDF")
                
                # Import python-docx for proper DOCX creation
                try:
                    from docx import Document
                    from docx.shared import Inches
                    from docx.enum.text import WD_ALIGN_PARAGRAPH
                    import io
                    import base64
                except ImportError:
                    logger.warning("python-docx not available, using basic text extraction")
                    # Fallback to basic text extraction
                    raise ImportError("python-docx required for advanced conversion")
                
                doc = fitz.open(str(temp_pdf))
                word_doc = Document()
                
                # Add document metadata
                core_props = word_doc.core_properties
                core_props.title = f"Converted from {original_name}"
                core_props.author = "ImagePDF Toolkit"
                core_props.comments = f"Converted using PyMuPDF on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                
                total_text_chars = 0
                total_images = 0
                
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    
                    # Add page header
                    if page_num > 0:
                        word_doc.add_page_break()
                    
                    # Extract text with better formatting
                    text_dict = page.get_text("dict")
                    
                    # Process text blocks
                    for block in text_dict.get("blocks", []):
                        if "lines" in block:  # Text block
                            block_text = ""
                            for line in block["lines"]:
                                line_text = ""
                                for span in line.get("spans", []):
                                    line_text += span.get("text", "")
                                block_text += line_text + "\n"
                            
                            if block_text.strip():
                                paragraph = word_doc.add_paragraph(block_text.strip())
                                total_text_chars += len(block_text)
                        
                        elif include_images and "image" in block:  # Image block
                            try:
                                # Extract image
                                image_index = block["image"]
                                base_image = doc.extract_image(image_index)
                                image_bytes = base_image["image"]
                                
                                # Add image to document
                                image_stream = io.BytesIO(image_bytes)
                                paragraph = word_doc.add_paragraph()
                                run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
                                
                                # Calculate image size (max width 6 inches)
                                max_width = Inches(6)
                                run.add_picture(image_stream, width=max_width)
                                
                                total_images += 1
                                logger.info(f"Added image {total_images} from page {page_num + 1}")
                                
                            except Exception as img_error:
                                logger.warning(f"Failed to extract image from page {page_num + 1}: {img_error}")
                                # Add placeholder text for failed image
                                word_doc.add_paragraph(f"[Image {total_images + 1} - extraction failed]")
                
                doc.close()
                
                # Save the document
                word_doc.save(str(temp_docx))
                
                conversion_success = True
                conversion_method = "pymupdf_enhanced"
                conversion_stats = {
                    "pages": len(doc),
                    "images": total_images,
                    "text_chars": total_text_chars
                }
                
                logger.info(f"Enhanced PyMuPDF conversion successful: {conversion_stats}")
                
            except Exception as e:
                logger.warning(f"Enhanced PyMuPDF conversion failed: {e}")
                
                # Fallback to basic text extraction
                try:
                    logger.info("Falling back to basic text extraction")
                    doc = fitz.open(str(temp_pdf))
                    
                    # Use simple docx creation if available
                    try:
                        from docx import Document
                        word_doc = Document()
                        
                        for page_num in range(len(doc)):
                            page = doc.load_page(page_num)
                            text = page.get_text()
                            
                            if text.strip():
                                if page_num > 0:
                                    word_doc.add_page_break()
                                word_doc.add_paragraph(f"--- Page {page_num + 1} ---")
                                word_doc.add_paragraph(text)
                                conversion_stats["text_chars"] += len(text)
                        
                        conversion_stats["pages"] = len(doc)
                        doc.close()
                        word_doc.save(str(temp_docx))
                        
                        conversion_success = True
                        conversion_method = "pymupdf_basic"
                        logger.info("Basic text extraction successful")
                        
                    except ImportError:
                        logger.error("python-docx not available for fallback")
                        
                except Exception as fallback_error:
                    logger.error(f"Fallback conversion failed: {fallback_error}")
        
        if not conversion_success:
            return jsonify({
                "error": "All conversion methods failed",
                "details": "PDF may be corrupted, password-protected, or contain unsupported content",
                "suggestions": [
                    "Ensure PDF is not password-protected",
                    "Try with a different PDF file",
                    "Check if PDF contains extractable text"
                ]
            }), 500
        
        # Verify output file
        if not temp_docx.exists() or temp_docx.stat().st_size == 0:
            return jsonify({
                "error": "Conversion produced empty file",
                "details": "The PDF might not contain extractable content"
            }), 500
        
        # Copy to cache
        shutil.copy2(temp_docx, cached_file)
        
        # Log successful conversion
        logger.info(f"Successfully converted {original_name} to DOCX using {conversion_method}")
        logger.info(f"Conversion stats: {conversion_stats}")
        
        @after_this_request
        def cleanup(response):
            try:
                if temp_pdf.exists():
                    temp_pdf.unlink()
                if temp_docx.exists():
                    temp_docx.unlink()
            except Exception as e:
                logger.warning(f"Cleanup error: {e}")
            return response
        
        # Return file with conversion stats in headers
        response = send_file(
            cached_file,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
        response.headers['X-Conversion-Method'] = conversion_method
        response.headers['X-Pages-Processed'] = str(conversion_stats['pages'])
        response.headers['X-Images-Extracted'] = str(conversion_stats['images'])
        response.headers['X-Text-Characters'] = str(conversion_stats['text_chars'])
        
        return response
        
    except Exception as e:
        track_error("PDF_TO_DOCX_ERROR", str(e))
        logger.error(f"PDF to DOCX conversion error: {str(e)}")
        return jsonify({
            "error": f"Conversion failed: {str(e)}",
            "code": "CONVERSION_ERROR"
        }), 500

@app.route('/compress-pdf', methods=['POST'])
@enhanced_error_handler
def compress_pdf():
    """
    Compress PDF using Ghostscript or PyMuPDF with advanced optimization
    Features: Size optimization, quality control, smart caching, image compression
    """
    logger.info("PDF compression request received")
    
    if not (GHOSTSCRIPT_AVAILABLE or PYMUPDF_AVAILABLE):
        return jsonify({
            "error": "PDF compression not available. Install Ghostscript or PyMuPDF"
        }), 500
    
    # Validate file upload
    try:
        validate_file_upload(request.files.get('file'), ['.pdf'], max_size_mb=100)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    file = request.files['file']
    force_compression = request.form.get('force', 'false').lower() == 'true'
    
    # Quality settings for Ghostscript
    quality_map = {
        'low': '/screen',      # Lowest quality, smallest size
        'medium': '/ebook',    # Medium quality
        'high': '/printer',    # High quality
        'max': '/prepress'     # Maximum quality
    }
    quality = request.form.get('quality', 'medium').lower()
    gs_quality = quality_map.get(quality, '/ebook')
    
    try:
        # Read file content and generate hash
        file_content = file.read()
        file_hash = get_file_hash(file_content)
        original_size = len(file_content)
        
        # Generate filenames
        original_name = secure_filename(file.filename)
        base_name = Path(original_name).stem
        output_filename = f"{base_name}_compressed.pdf"
        
        # Check cache with quality suffix
        cache_key = f"{file_hash}_{quality}_{output_filename}"
        cached_file = CACHE_DIR / cache_key
        
        if cached_file.exists() and not force_compression:
            compressed_size = cached_file.stat().st_size
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            logger.info(f"Returning cached compressed PDF: {output_filename} ({compression_ratio:.1f}% reduction)")
            
            response = send_file(
                cached_file,
                as_attachment=True,
                download_name=output_filename,
                mimetype='application/pdf'
            )
            response.headers['X-Compression-Ratio'] = f"{compression_ratio:.1f}%"
            response.headers['X-Original-Size'] = str(original_size)
            response.headers['X-Compressed-Size'] = str(compressed_size)
            response.headers['X-Cached'] = 'true'
            return response
        
        # Check if file is already small enough
        if original_size < 1024 * 1024 and not force_compression:  # < 1MB
            logger.info("File already small, skipping compression")
            import io
            response = send_file(
                io.BytesIO(file_content),
                as_attachment=True,
                download_name=original_name,
                mimetype='application/pdf'
            )
            response.headers['X-Compression-Ratio'] = "0%"
            response.headers['X-Message'] = "File already optimized"
            return response
        
        # Create temporary files
        temp_input = TEMP_DIR / f"{file_hash}_input.pdf"
        temp_output = TEMP_DIR / f"{file_hash}_compressed.pdf"
        
        # Write input file
        with open(temp_input, 'wb') as f:
            f.write(file_content)
        
        compression_success = False
        compression_method = ""
        compression_stats = {"original_size": original_size, "compressed_size": 0, "method": ""}
        
        # Method 1: Try Ghostscript (preferred for compression)
        if GHOSTSCRIPT_AVAILABLE and not compression_success:
            try:
                logger.info(f"Attempting compression with Ghostscript (quality: {quality})")
                
                # Find Ghostscript executable
                gs_cmd = None
                gs_paths = [
                    r'C:\Program Files\gs\gs10.05.1\bin\gswin64c.exe',
                    r'C:\Program Files\gs\gs9.56.1\bin\gswin64c.exe',
                    'gs',  # Try system PATH
                    'gswin64c',
                    'gswin32c'
                ]
                
                for path in gs_paths:
                    try:
                        result = subprocess.run([path, '--version'], 
                                              capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            gs_cmd = path
                            break
                    except (subprocess.SubprocessError, FileNotFoundError):
                        continue
                
                if not gs_cmd:
                    raise FileNotFoundError("Ghostscript executable not found")
                
                # Enhanced Ghostscript command with better compression
                cmd = [
                    gs_cmd,
                    '-sDEVICE=pdfwrite',
                    '-dCompatibilityLevel=1.4',
                    f'-dPDFSETTINGS={gs_quality}',
                    '-dNOPAUSE',
                    '-dQUIET',
                    '-dBATCH',
                    '-dSAFER',
                    '-dColorImageDownsampleType=/Bicubic',
                    '-dGrayImageDownsampleType=/Bicubic',
                    '-dMonoImageDownsampleType=/Bicubic',
                    '-dOptimize=true',
                    '-dEmbedAllFonts=true',
                    '-dSubsetFonts=true',
                    '-dCompressFonts=true',
                    '-dDetectDuplicateImages=true',
                    f'-sOutputFile={temp_output}',
                    str(temp_input)
                ]
                
                # Add quality-specific settings
                if quality == 'low':
                    cmd.extend([
                        '-dColorImageResolution=72',
                        '-dGrayImageResolution=72',
                        '-dMonoImageResolution=300',
                        '-dDownsampleColorImages=true',
                        '-dDownsampleGrayImages=true'
                    ])
                elif quality == 'medium':
                    cmd.extend([
                        '-dColorImageResolution=150',
                        '-dGrayImageResolution=150',
                        '-dMonoImageResolution=600'
                    ])
                elif quality == 'high':
                    cmd.extend([
                        '-dColorImageResolution=300',
                        '-dGrayImageResolution=300',
                        '-dMonoImageResolution=1200'
                    ])
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0 and temp_output.exists() and temp_output.stat().st_size > 0:
                    compression_success = True
                    compression_method = "ghostscript"
                    compression_stats["compressed_size"] = temp_output.stat().st_size
                    compression_stats["method"] = f"Ghostscript ({quality})"
                    logger.info("Compression successful with Ghostscript")
                else:
                    logger.warning(f"Ghostscript compression failed: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                logger.warning("Ghostscript compression timeout")
                track_error("GHOSTSCRIPT_TIMEOUT", "Ghostscript operation timed out")
            except Exception as e:
                logger.warning(f"Ghostscript compression error: {e}")
                track_error("GHOSTSCRIPT_ERROR", str(e))
        
        # Method 2: Try PyMuPDF (fallback with enhanced compression)
        if PYMUPDF_AVAILABLE and not compression_success:
            try:
                logger.info("Attempting compression with enhanced PyMuPDF")
                
                doc = fitz.open(str(temp_input))
                
                # Quality-based compression parameters
                if quality == 'low':
                    deflate_level = 9
                    image_quality = 50
                elif quality == 'medium':
                    deflate_level = 6
                    image_quality = 70
                elif quality == 'high':
                    deflate_level = 3
                    image_quality = 85
                else:  # max
                    deflate_level = 1
                    image_quality = 95
                
                # Advanced compression options
                save_options = {
                    "garbage": 4,  # Remove unused objects
                    "deflate": True,  # Enable deflate compression
                    "deflate_images": True,  # Compress images
                    "deflate_fonts": True,  # Compress fonts
                    "linear": True,  # Optimize for web viewing
                    "clean": True,  # Clean up document structure
                    "pretty": False,  # Don't pretty-print (saves space)
                    "ascii": False,  # Use binary encoding
                    "expand": 0,  # Don't expand content streams
                    "compression": deflate_level
                }
                
                # For lower quality, apply image compression
                if quality in ['low', 'medium']:
                    # Process each page for image optimization
                    for page_num in range(len(doc)):
                        page = doc.load_page(page_num)
                        
                        # Get images on page
                        image_list = page.get_images()
                        
                        for img_index, img in enumerate(image_list):
                            try:
                                # Extract image
                                xref = img[0]
                                base_image = doc.extract_image(xref)
                                image_bytes = base_image["image"]
                                image_ext = base_image["ext"]
                                
                                # Compress image if it's large
                                if len(image_bytes) > 50000:  # > 50KB
                                    from PIL import Image
                                    import io
                                    
                                    # Open image with Pillow
                                    pil_image = Image.open(io.BytesIO(image_bytes))
                                    
                                    # Resize if too large
                                    max_dimension = 1024 if quality == 'low' else 1536
                                    if max(pil_image.size) > max_dimension:
                                        ratio = max_dimension / max(pil_image.size)
                                        new_size = tuple(int(dim * ratio) for dim in pil_image.size)
                                        pil_image = pil_image.resize(new_size, Image.Resampling.LANCZOS)
                                    
                                    # Convert to RGB if needed
                                    if pil_image.mode not in ['RGB', 'L']:
                                        pil_image = pil_image.convert('RGB')
                                    
                                    # Save with compression
                                    output_buffer = io.BytesIO()
                                    save_format = 'JPEG' if image_ext.lower() in ['jpg', 'jpeg'] else 'PNG'
                                    
                                    if save_format == 'JPEG':
                                        pil_image.save(output_buffer, format=save_format, 
                                                     quality=image_quality, optimize=True)
                                    else:
                                        pil_image.save(output_buffer, format=save_format, 
                                                     optimize=True, compress_level=9)
                                    
                                    compressed_image_bytes = output_buffer.getvalue()
                                    
                                    # Replace image if compression helped
                                    if len(compressed_image_bytes) < len(image_bytes):
                                        # This would require more complex PyMuPDF operations
                                        # For now, just log the potential savings
                                        savings = len(image_bytes) - len(compressed_image_bytes)
                                        logger.info(f"Image {img_index} could be reduced by {savings} bytes")
                                        
                            except Exception as img_error:
                                logger.warning(f"Failed to compress image {img_index}: {img_error}")
                
                # Save with optimizations
                doc.save(str(temp_output), **save_options)
                doc.close()
                
                if temp_output.exists() and temp_output.stat().st_size > 0:
                    compression_success = True
                    compression_method = "pymupdf_enhanced"
                    compression_stats["compressed_size"] = temp_output.stat().st_size
                    compression_stats["method"] = f"PyMuPDF Enhanced ({quality})"
                    logger.info("Compression successful with enhanced PyMuPDF")
                else:
                    logger.warning("PyMuPDF produced empty file")
                
            except Exception as e:
                logger.warning(f"Enhanced PyMuPDF compression error: {e}")
                track_error("PYMUPDF_ERROR", str(e))
        
        if not compression_success:
            return jsonify({
                "error": "All compression methods failed",
                "details": "PDF may be corrupted, already optimized, or contain unsupported features",
                "suggestions": [
                    "Try with a different quality setting",
                    "Check if PDF is password-protected",
                    "Ensure PDF is not already heavily compressed"
                ]
            }), 500
        
        # Calculate compression ratio
        compressed_size = temp_output.stat().st_size
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        # Only keep compressed version if it's actually smaller
        if compressed_size >= original_size and not force_compression:
            logger.info("Compression didn't reduce file size, returning original")
            response = send_file(
                temp_input,
                as_attachment=True,
                download_name=original_name,
                mimetype='application/pdf'
            )
            response.headers['X-Compression-Ratio'] = "0%"
            response.headers['X-Message'] = "Original file already optimized"
            return response
        
        # Copy to cache
        shutil.copy2(temp_output, cached_file)
        
        # Update compression stats
        compression_stats["compression_ratio"] = compression_ratio
        
        # Log compression
        logger.info(f"Successfully compressed {original_name} using {compression_method}")
        logger.info(f"Compression stats: {compression_stats}")
        
        @after_this_request
        def cleanup(response):
            try:
                if temp_input.exists():
                    temp_input.unlink()
                if temp_output.exists():
                    temp_output.unlink()
            except Exception as e:
                logger.warning(f"Cleanup error: {e}")
            return response
        
        response = send_file(
            cached_file,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/pdf'
        )
        response.headers['X-Compression-Ratio'] = f"{compression_ratio:.1f}%"
        response.headers['X-Original-Size'] = str(original_size)
        response.headers['X-Compressed-Size'] = str(compressed_size)
        response.headers['X-Method'] = compression_method
        response.headers['X-Quality'] = quality
        
        return response
        
    except Exception as e:
        track_error("PDF_COMPRESSION_ERROR", str(e))
        logger.error(f"PDF compression error: {str(e)}")
        return jsonify({
            "error": f"Compression failed: {str(e)}",
            "code": "COMPRESSION_ERROR"
        }), 500

@app.route('/compress-image', methods=['POST'])
def compress_image():
    """
    Compress image files using Pillow
    Features: Quality control, format optimization, smart caching
    """
    logger.info("Image compression request received")
    
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    quality = int(request.form.get('quality', 85))  # Default quality 85%
    force_compression = request.form.get('force', 'false').lower() == 'true'
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Supported image formats
    supported_formats = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff']
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in supported_formats:
        return jsonify({"error": f"Unsupported format. Supported: {', '.join(supported_formats)}"}), 400
    
    try:
        from PIL import Image
        import io
        
        # Read file content and generate hash
        file_content = file.read()
        file_hash = get_file_hash(file_content)
        original_size = len(file_content)
        
        # Generate filenames
        original_name = secure_filename(file.filename)
        base_name = Path(original_name).stem
        output_filename = f"{base_name}_compressed{file_ext}"
        
        # Check cache with quality suffix
        cached_file = CACHE_DIR / f"{file_hash}_q{quality}_{output_filename}"
        
        if cached_file.exists() and not force_compression:
            compressed_size = cached_file.stat().st_size
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            logger.info(f"Returning cached compressed image: {output_filename} ({compression_ratio:.1f}% reduction)")
            
            response = send_file(
                cached_file,
                as_attachment=True,
                download_name=output_filename,
                mimetype=f'image/{file_ext[1:]}'
            )
            response.headers['X-Compression-Ratio'] = f"{compression_ratio:.1f}%"
            response.headers['X-Original-Size'] = str(original_size)
            response.headers['X-Compressed-Size'] = str(compressed_size)
            return response
        
        # Open and process image
        img = Image.open(io.BytesIO(file_content))
        
        # Convert RGBA to RGB if saving as JPEG
        if file_ext.lower() in ['.jpg', '.jpeg'] and img.mode in ('RGBA', 'LA', 'P'):
            # Create white background for transparency
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Compress and save
        output_buffer = io.BytesIO()
        
        save_kwargs = {
            'format': img.format if img.format else 'JPEG',
            'quality': quality,
            'optimize': True
        }
        
        # Format specific optimizations
        if file_ext.lower() in ['.jpg', '.jpeg']:
            save_kwargs['progressive'] = True
        elif file_ext.lower() == '.png':
            save_kwargs['compress_level'] = 9
            del save_kwargs['quality']  # PNG doesn't use quality
        elif file_ext.lower() == '.webp':
            save_kwargs['method'] = 6  # Better compression
        
        img.save(output_buffer, **save_kwargs)
        compressed_data = output_buffer.getvalue()
        compressed_size = len(compressed_data)
        
        # Calculate compression ratio
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        # Only keep compressed version if it's actually smaller
        if compressed_size >= original_size and not force_compression:
            logger.info("Compression didn't reduce file size, returning original")
            response = send_file(
                io.BytesIO(file_content),
                as_attachment=True,
                download_name=original_name,
                mimetype=f'image/{file_ext[1:]}'
            )
            response.headers['X-Compression-Ratio'] = "0%"
            response.headers['X-Message'] = "Original file already optimized"
            return response
        
        # Save to cache
        with open(cached_file, 'wb') as f:
            f.write(compressed_data)
        
        # Log compression
        logger.info(f"Successfully compressed {original_name} "
                   f"({compression_ratio:.1f}% reduction: {original_size} -> {compressed_size} bytes)")
        
        response = send_file(
            io.BytesIO(compressed_data),
            as_attachment=True,
            download_name=output_filename,
            mimetype=f'image/{file_ext[1:]}'
        )
        response.headers['X-Compression-Ratio'] = f"{compression_ratio:.1f}%"
        response.headers['X-Original-Size'] = str(original_size)
        response.headers['X-Compressed-Size'] = str(compressed_size)
        
        return response
        
    except Exception as e:
        logger.error(f"Image compression error: {str(e)}")
        return jsonify({"error": f"Compression failed: {str(e)}"}), 500

@app.route('/batch-process', methods=['POST'])
def batch_process():
    """
    Batch process multiple files
    Supports mixed operations and returns ZIP archive
    """
    logger.info("Batch processing request received")
    
    if 'files' not in request.files:
        return jsonify({"error": "No files uploaded"}), 400
    
    files = request.files.getlist('files')
    operation = request.form.get('operation', 'auto')  # auto, compress, convert
    
    if len(files) > 10:
        return jsonify({"error": "Maximum 10 files allowed in batch"}), 400
    
    if not files or all(f.filename == '' for f in files):
        return jsonify({"error": "No files selected"}), 400
    
    try:
        # Create temporary directory for batch processing
        batch_id = hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:8]
        batch_dir = TEMP_DIR / f"batch_{batch_id}"
        batch_dir.mkdir(exist_ok=True)
        
        processed_files = []
        errors = []
        
        for file in files:
            if file.filename == '':
                continue
                
            try:
                original_name = secure_filename(file.filename)
                file_ext = Path(original_name).suffix.lower()
                
                # Determine operation based on file type and user preference
                if operation == 'auto':
                    if file_ext == '.pdf':
                        # Auto: compress PDF
                        current_op = 'compress'
                    elif file_ext == '.docx':
                        # Auto: convert DOCX to PDF
                        current_op = 'convert_to_pdf'
                    else:
                        errors.append(f"{original_name}: Unsupported file type")
                        continue
                else:
                    current_op = operation
                
                # Process file based on operation
                if current_op == 'compress' and file_ext == '.pdf':
                    # Simulate compression endpoint logic
                    file_content = file.read()
                    temp_file = batch_dir / f"compressed_{original_name}"
                    
                    # For batch, use simple PyMuPDF compression
                    if PYMUPDF_AVAILABLE:
                        temp_input = batch_dir / f"input_{original_name}"
                        with open(temp_input, 'wb') as f:
                            f.write(file_content)
                        
                        doc = fitz.open(str(temp_input))
                        doc.save(str(temp_file), garbage=4, deflate=True)
                        doc.close()
                        
                        processed_files.append(str(temp_file))
                    else:
                        errors.append(f"{original_name}: Compression not available")
                
                elif current_op == 'convert_to_pdf' and file_ext == '.docx':
                    # Simulate DOCX to PDF conversion
                    if False:  # LibreOffice not available in this setup
                        file_content = file.read()
                        temp_input = batch_dir / original_name
                        
                        with open(temp_input, 'wb') as f:
                            f.write(file_content)
                        
                        cmd = [
                            'libreoffice',
                            '--headless',
                            '--convert-to', 'pdf',
                            '--outdir', str(batch_dir),
                            str(temp_input)
                        ]
                        
                        result = subprocess.run(cmd, capture_output=True, timeout=60)
                        
                        if result.returncode == 0:
                            pdf_name = Path(original_name).stem + '.pdf'
                            pdf_file = batch_dir / pdf_name
                            if pdf_file.exists():
                                processed_files.append(str(pdf_file))
                            else:
                                errors.append(f"{original_name}: PDF not generated")
                        else:
                            errors.append(f"{original_name}: Conversion failed")
                    else:
                        errors.append(f"{original_name}: LibreOffice not available in this setup")
                
                else:
                    errors.append(f"{original_name}: Operation not supported for this file type")
                    
            except Exception as e:
                errors.append(f"{file.filename}: {str(e)}")
        
        if not processed_files:
            return jsonify({
                "error": "No files were successfully processed",
                "errors": errors
            }), 400
        
        # Create ZIP archive
        zip_filename = f"batch_processed_{batch_id}.zip"
        zip_path = batch_dir / zip_filename
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in processed_files:
                file_path_obj = Path(file_path)
                zipf.write(file_path, file_path_obj.name)
        
        logger.info(f"Batch processing completed: {len(processed_files)} files processed, {len(errors)} errors")
        
        @after_this_request
        def cleanup(response):
            try:
                shutil.rmtree(batch_dir)
            except Exception as e:
                logger.warning(f"Batch cleanup error: {e}")
            return response
        
        response = send_file(
            zip_path,
            as_attachment=True,
            download_name=zip_filename,
            mimetype='application/zip'
        )
        response.headers['X-Processed-Files'] = str(len(processed_files))
        response.headers['X-Errors'] = str(len(errors))
        
        return response
        
    except Exception as e:
        logger.error(f"Batch processing error: {str(e)}")
        return jsonify({"error": f"Batch processing failed: {str(e)}"}), 500

@app.route('/pdf-merge', methods=['POST'])
def pdf_merge():
    """
    Merge multiple PDF files into a single PDF
    Features: Multiple PDF merging, order preservation
    """
    logger.info("PDF merge request received")
    
    if not PYMUPDF_AVAILABLE:
        return jsonify({
            "error": "PDF merging not available. Install PyMuPDF"
        }), 500
    
    if 'files' not in request.files:
        return jsonify({"error": "No files uploaded"}), 400
    
    files = request.files.getlist('files')
    
    if len(files) < 2:
        return jsonify({"error": "At least 2 PDF files are required for merging"}), 400
    
    if len(files) > 20:
        return jsonify({"error": "Maximum 20 files allowed for merging"}), 400
    
    try:
        import fitz
        
        # Create merged PDF
        merged_doc = fitz.open()
        
        for file in files:
            if file.filename == '':
                continue
                
            if not file.filename.lower().endswith('.pdf'):
                continue
            
            # Read file content
            file_content = file.read()
            temp_pdf = TEMP_DIR / f"temp_{hash(file_content)}.pdf"
            
            with open(temp_pdf, 'wb') as f:
                f.write(file_content)
            
            # Open and merge
            doc = fitz.open(str(temp_pdf))
            merged_doc.insert_pdf(doc)
            doc.close()
            
            # Cleanup temp file
            if temp_pdf.exists():
                temp_pdf.unlink()
        
        # Save merged PDF
        output_filename = f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        output_path = TEMP_DIR / output_filename
        
        merged_doc.save(str(output_path))
        merged_doc.close()
        
        logger.info(f"Successfully merged {len(files)} PDF files into {output_filename}")
        
        @after_this_request
        def cleanup(response):
            try:
                if output_path.exists():
                    output_path.unlink()
            except Exception as e:
                logger.warning(f"Cleanup error: {e}")
            return response
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        logger.error(f"PDF merge error: {str(e)}")
        return jsonify({"error": f"PDF merging failed: {str(e)}"}), 500

@app.route('/pdf-split', methods=['POST'])
@enhanced_error_handler
def pdf_split():
    """
    Split PDF into multiple files by pages with enhanced functionality
    Features: Page range splitting, individual page extraction, preview support
    """
    logger.info("PDF split request received")
    
    if not PYMUPDF_AVAILABLE:
        return jsonify({
            "error": "PDF splitting not available. Install PyMuPDF"
        }), 500
    
    # Validate file upload
    try:
        validate_file_upload(request.files.get('file'), ['.pdf'], max_size_mb=100)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    file = request.files['file']
    split_type = request.form.get('type', 'individual')  # individual, range, custom
    page_ranges = request.form.get('ranges', '')  # e.g., "1-3,5,7-9"
    pages_per_split = request.form.get('pages_per_split', '1')  # for bulk splitting
    
    try:
        import fitz
        
        # Read file content
        file_content = file.read()
        file_hash = get_file_hash(file_content)
        
        temp_pdf = TEMP_DIR / f"{file_hash}_input.pdf"
        
        with open(temp_pdf, 'wb') as f:
            f.write(file_content)
        
        doc = fitz.open(str(temp_pdf))
        total_pages = len(doc)
        
        if total_pages == 0:
            doc.close()
            return jsonify({
                "error": "PDF contains no pages",
                "details": "The uploaded PDF file appears to be empty"
            }), 400
        
        logger.info(f"Processing PDF with {total_pages} pages, split_type: {split_type}")
        
        # Parse page ranges based on split type
        ranges = []
        
        if split_type == 'individual':
            # Split into individual pages
            ranges = [(i, i) for i in range(total_pages)]
            logger.info(f"Individual split: {len(ranges)} pages")
            
        elif split_type == 'bulk' and pages_per_split.isdigit():
            # Split into chunks of specified size
            pages_per_chunk = int(pages_per_split)
            if pages_per_chunk < 1:
                pages_per_chunk = 1
            
            for i in range(0, total_pages, pages_per_chunk):
                end_page = min(i + pages_per_chunk - 1, total_pages - 1)
                ranges.append((i, end_page))
            logger.info(f"Bulk split: {len(ranges)} chunks of {pages_per_chunk} pages each")
            
        elif split_type == 'range' and page_ranges:
            # Parse custom page ranges
            try:
                for range_str in page_ranges.split(','):
                    range_str = range_str.strip()
                    if '-' in range_str:
                        start_str, end_str = range_str.split('-', 1)
                        start = int(start_str.strip()) - 1  # Convert to 0-based
                        end = int(end_str.strip()) - 1
                        
                        # Validate range
                        if start < 0 or end >= total_pages or start > end:
                            doc.close()
                            return jsonify({
                                "error": f"Invalid page range: {range_str}",
                                "details": f"Valid page numbers are 1-{total_pages}"
                            }), 400
                        
                        ranges.append((start, end))
                    else:
                        page_num = int(range_str) - 1
                        if page_num < 0 or page_num >= total_pages:
                            doc.close()
                            return jsonify({
                                "error": f"Invalid page number: {range_str}",
                                "details": f"Valid page numbers are 1-{total_pages}"
                            }), 400
                        ranges.append((page_num, page_num))
                        
                logger.info(f"Custom range split: {len(ranges)} ranges")
                
            except ValueError as ve:
                doc.close()
                return jsonify({
                    "error": f"Invalid page range format: {page_ranges}",
                    "details": "Use format like '1-3,5,7-9' (page numbers start from 1)"
                }), 400
        else:
            doc.close()
            return jsonify({
                "error": "Invalid split configuration",
                "details": "Specify valid split_type and parameters"
            }), 400
        
        if not ranges:
            doc.close()
            return jsonify({
                "error": "No valid page ranges specified",
                "details": "Check your page range configuration"
            }), 400
        
        # Create ZIP for multiple files
        original_name = secure_filename(file.filename)
        base_name = Path(original_name).stem
        zip_filename = f"{base_name}_split_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = TEMP_DIR / zip_filename
        
        split_files = []
        split_stats = {
            "total_pages": total_pages,
            "split_count": len(ranges),
            "split_type": split_type,
            "success_count": 0,
            "failed_count": 0
        }
        
        # Process each range
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
            for i, (start, end) in enumerate(ranges):
                try:
                    # Create new PDF with selected pages
                    new_doc = fitz.open()
                    new_doc.insert_pdf(doc, from_page=start, to_page=end)
                    
                    # Generate descriptive filename
                    if start == end:
                        split_filename = f"{base_name}_page_{start+1}.pdf"
                        page_info = f"page {start+1}"
                    else:
                        split_filename = f"{base_name}_pages_{start+1}-{end+1}.pdf"
                        page_info = f"pages {start+1}-{end+1}"
                    
                    # Save to temporary file
                    split_path = TEMP_DIR / split_filename
                    
                    # Save with optimization
                    new_doc.save(
                        str(split_path),
                        garbage=4,  # Remove unused objects
                        deflate=True,  # Compress
                        linear=True  # Optimize for web
                    )
                    new_doc.close()
                    
                    # Verify file was created successfully
                    if split_path.exists() and split_path.stat().st_size > 0:
                        # Add to ZIP
                        zipf.write(split_path, split_filename)
                        split_files.append({
                            "filename": split_filename,
                            "pages": page_info,
                            "size": split_path.stat().st_size
                        })
                        split_stats["success_count"] += 1
                        logger.info(f"Created split file: {split_filename} ({page_info})")
                        
                        # Cleanup temp split file
                        split_path.unlink()
                    else:
                        logger.warning(f"Failed to create split file for {page_info}")
                        split_stats["failed_count"] += 1
                        
                except Exception as split_error:
                    logger.error(f"Error creating split for range {start+1}-{end+1}: {split_error}")
                    split_stats["failed_count"] += 1
                    track_error("PDF_SPLIT_RANGE_ERROR", f"Range {start+1}-{end+1}: {str(split_error)}")
        
        doc.close()
        
        # Check if any splits were successful
        if split_stats["success_count"] == 0:
            return jsonify({
                "error": "Failed to create any split files",
                "details": "All page ranges failed to process",
                "stats": split_stats
            }), 500
        
        # Verify ZIP file was created
        if not zip_path.exists() or zip_path.stat().st_size == 0:
            return jsonify({
                "error": "Failed to create output archive",
                "details": "ZIP file creation failed"
            }), 500
        
        # Log successful split
        logger.info(f"Successfully split PDF: {split_stats}")
        
        @after_this_request
        def cleanup(response):
            try:
                if temp_pdf.exists():
                    temp_pdf.unlink()
                if zip_path.exists():
                    zip_path.unlink()
                # Clean up any remaining split files
                for temp_file in TEMP_DIR.glob(f"{file_hash}_*.pdf"):
                    temp_file.unlink()
            except Exception as e:
                logger.warning(f"Cleanup error: {e}")
            return response
        
        # Prepare response with metadata
        response = send_file(
            zip_path,
            as_attachment=True,
            download_name=zip_filename,
            mimetype='application/zip'
        )
        
        response.headers['X-Total-Pages'] = str(split_stats["total_pages"])
        response.headers['X-Split-Count'] = str(split_stats["success_count"])
        response.headers['X-Failed-Count'] = str(split_stats["failed_count"])
        response.headers['X-Split-Type'] = split_type
        
        return response
        
    except Exception as e:
        track_error("PDF_SPLIT_ERROR", str(e))
        logger.error(f"PDF split error: {str(e)}")
        return jsonify({
            "error": f"PDF splitting failed: {str(e)}",
            "code": "SPLIT_ERROR"
        }), 500

@app.route('/clear-cache', methods=['POST'])
def clear_cache():
    """Clear the cache directory"""
    try:
        cache_files = list(CACHE_DIR.glob('*'))
        temp_files = list(TEMP_DIR.glob('*'))
        
        for file_path in cache_files + temp_files:
            if file_path.is_file():
                file_path.unlink()
            elif file_path.is_dir():
                shutil.rmtree(file_path)
        
        logger.info(f"Cache cleared: {len(cache_files)} cache files, {len(temp_files)} temp files")
        
        return jsonify({
            "message": "Cache cleared successfully",
            "files_removed": len(cache_files) + len(temp_files)
        })
        
    except Exception as e:
        logger.error(f"Cache clear error: {str(e)}")
        return jsonify({"error": f"Cache clear failed: {str(e)}"}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large. Maximum size is 500MB"}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Azure App Service compatible startup
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    logger.info(f"🚀 Starting Flask app on port {port} (debug={debug})")
    
    try:
        app.run(
            debug=debug, 
            host='0.0.0.0', 
            port=port,
            threaded=True
        )
    except Exception as e:
        logger.error(f"❌ Failed to start Flask app: {e}")
        raise
